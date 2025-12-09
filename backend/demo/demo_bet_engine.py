# backend/demo/demo_bet_engine.py
import json
from decimal import Decimal, getcontext, ROUND_HALF_UP
from datetime import datetime
from backend.demo.demo_storage import save_bet, inc_counter, get_daily_counters, inc_consecutive_losses, settle_bet, set_setting, get_setting
from backend.demo.decision_engine import evaluate_and_create_ticket
from backend.demo.demo_storage import get_setting

# set decimal precision
getcontext().prec = 10

# Bank stored as setting
def get_bank():
    b = get_setting("bank_balance")
    return Decimal(b) if b else Decimal("1000.00")

def set_bank(value):
    set_setting("bank_balance", str(value))

def _to_decimal(x):
    try:
        return Decimal(str(x))
    except:
        return Decimal("0")

def calculate_stake_hybrid(bank: Decimal, settings: dict, confidence: float, odds: float):
    """
    Hybrid stake calculation: fractional Kelly scaled by confidence, with caps.
    Formula:
      - b = odds - 1
      - p = estimated probability (confidence)
      - q = 1 - p
      - kelly_fraction = max(0, (b*p - q) / b)
      - hybrid_fraction = kelly_fraction * confidence   # confidence scales aggressiveness
      - stake = bank * hybrid_fraction
    Caps and safety:
      - Apply max_pct_of_bank cap (settings 'max_stake_pct_of_bank', default 0.05)
      - Apply minimal stake (settings 'min_stake', default 1.0)
      - Round to 2 decimals
    """
    # safety conversions
    bank = _to_decimal(bank)
    confidence = float(confidence)
    odds = float(odds) if odds and odds > 1 else 1.01

    p = confidence
    q = 1.0 - p
    b = max(odds - 1.0, 0.0001)

    # Kelly fraction (unbounded negative possible -> clip to 0)
    kelly_fraction = max(0.0, (b * p - q) / b)

    # scale Kelly by confidence to get hybrid aggressiveness
    hybrid_fraction = kelly_fraction * p

    # fallback to conservative stake_pct_of_bank if kelly gives zero
    default_pct = float(settings.get("stake_pct_of_bank", 0.02))
    if hybrid_fraction <= 0:
        hybrid_fraction = default_pct

    # apply maximum cap
    max_pct = float(settings.get("max_stake_pct_of_bank", 0.05))
    hybrid_fraction = min(hybrid_fraction, max_pct)

    stake = (bank * Decimal(str(hybrid_fraction))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    min_stake = Decimal(str(settings.get("min_stake", 1.0)))
    if stake < min_stake:
        stake = min_stake

    return float(stake)

def calculate_stake(bank: Decimal, settings: dict, confidence: float, odds: float):
    """
    Backward-compatible wrapper. Currently uses hybrid Kelly+confidence approach.
    """
    return calculate_stake_hybrid(bank, settings, confidence, odds)

def place_auto_demo(team_candidates, settings):
    # check daily limits & loss rules
    counters = get_daily_counters()
    if int(counters["multis"]) >= int(settings.get("max_multis_per_day",4)):
        return {"error":"max_multis_reached"}
    if int(counters["consecutive_losses"]) >= 2 and not settings.get("allow_after_two_losses", False):
        return {"error":"blocked_due_to_losses"}

    # decide ticket
    ticket = evaluate_and_create_ticket(team_candidates, settings)
    if not ticket:
        return {"status":"no_ticket_meets_threshold"}

    bank = get_bank()
    if ticket["type"] == "MULTI":
        confidence = ticket["confidence"]
        odds = ticket.get("compound_odd", 1.0)
        stake = calculate_stake(bank, settings, confidence, odds)
        bet = {
            "match_id": f"multi_{datetime.utcnow().timestamp()}",
            "teams": ticket["team"],
            "market": "MULTI",
            "bet_type": "MULTI",
            "selections_json": json.dumps(ticket["selections"]),
            "stake": stake,
            "odds": odds,
            "probability": ticket["confidence"],
            "confidence": ticket["confidence"],
            "justification": f"Multi built from team {ticket['team']} using markets: concatenated patterns"
        }
        bet_id = save_bet(bet)
        inc_counter("multis", 1)
        # debit bank
        new_balance = float(Decimal(bank) - Decimal(str(stake)))
        set_bank(new_balance)
        return {"placed":True, "bet_id":bet_id, "stake": stake, "new_balance": new_balance}
    else:
        # single
        s = ticket["selection"]
        confidence = s.get("confidence", s.get("probability", 0.0))
        odds = s.get("recommended_odd", 1.0)
        stake = calculate_stake(bank, settings, confidence, odds)
        bet = {
            "match_id": f"single_{datetime.utcnow().timestamp()}",
            "teams": f"{s.get('event',{}).get('home')} vs {s.get('event',{}).get('away')}",
            "market": s.get("market"),
            "bet_type": "SINGLE",
            "selections_json": json.dumps(s),
            "stake": stake,
            "odds": odds,
            "probability": s.get("probability"),
            "confidence": confidence,
            "justification": f"Auto single: reason {s.get('reason')}"
        }
        bet_id = save_bet(bet)
        inc_counter("singles",1)
        new_balance = float(Decimal(bank) - Decimal(str(stake)))
        set_bank(new_balance)
        return {"placed":True, "bet_id":bet_id, "stake": stake, "new_balance": new_balance}
