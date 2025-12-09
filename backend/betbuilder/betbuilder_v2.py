
# backend/betbuilder/betbuilder_v2.py
from typing import List, Dict, Any
from backend.services import demo_engine
from backend.demo.decision_engine import build_multi_from_team, score_selection
import math

def compute_selection_confidence(selection: Dict[str, Any]) -> float:
    # selection assumed produced by demo_engine.simulate_prediction
    return float(selection.get("confidence") or selection.get("probability") or 0.0)

def compute_compound_confidence(selections: List[Dict[str, Any]]) -> float:
    # Combine confidences conservatively — use geometric mean to penalize low-confidence legs
    probs = [max(0.01, compute_selection_confidence(s)) for s in selections]
    # geometric mean
    prod = 1.0
    for p in probs:
        prod *= p
    gm = prod ** (1.0 / len(probs)) if probs else 0.0
    return round(gm, 4)

def compute_total_odd(selections: List[Dict[str, Any]]) -> float:
    total = 1.0
    for s in selections:
        odd = s.get("recommended_odd") or s.get("odd") or 1.0
        try:
            total *= float(odd)
        except:
            total *= 1.0
    return round(total, 4)

def build_ticket_from_teams(teams: List[str], markets_per_team:int=2, max_teams:int=10) -> Dict[str,Any]:
    # builds a multi-ticket across up to max_teams teams, picking markets_per_team selections per team
    selections = []
    included = teams[:max_teams]
    per_match = []
    for team in included:
        # create a few selections for the team using demo_engine
        team_selections = []
        for i in range(markets_per_team):
            sel = demo_engine.simulate_prediction(event={"home":team, "away":"Opponent"})
            team_selections.append(sel)
        per_match.append({"team": team, "selections": team_selections})
        for s in team_selections:
            selections.append(s)
    confidence = compute_compound_confidence(selections)
    total_odd = compute_total_odd(selections)
    ticket = {
        "ticket_id": f"v2_" + str(abs(hash(tuple(teams))))[:12],
        "created_at": None,
        "matches": per_match,
        "selections_flat": selections,
        "total_odd": total_odd,
        "confidence": confidence,
        "status": "draft"
    }
    return ticket

def ticket_edit_apply(ticket: Dict[str,Any], edits: Dict[str,Any]) -> Dict[str,Any]:
    # edits may change markets per match or odd overrides; recompute confidence and odd
    # simplistic: allow overriding recommended_odd in flattened selections by index
    overrides = edits.get("overrides", {})
    for idx, v in overrides.items():
        try:
            i = int(idx)
            ticket["selections_flat"][i]["recommended_odd"] = float(v)
        except Exception:
            continue
    ticket["total_odd"] = compute_total_odd(ticket["selections_flat"])
    ticket["confidence"] = compute_compound_confidence(ticket["selections_flat"])
    return ticket
