import json, datetime
from services.accounts import get_account, adjust_balance, create_account
from services.justifications import save_justification
from services.db import cursor
from math import floor

DEFAULTS = {
    "min_confidence_for_bet": 0.80,
    "max_daily_multiples": 4,
    "max_daily_singles": 4,
    "max_multiples_per_bet": 10,
    "fraction_of_bank_per_bet": 0.02,
    "pause_after_losses": 2
}

def count_today_bets(account_type, market_type):
    cur = cursor()
    today = datetime.date.today()
    cur.execute("""SELECT count(*) as c FROM betslips WHERE account_type=%s AND market_type=%s AND created_at::date=%s""", (account_type, market_type, today))
    res = cur.fetchone()
    return res['c'] if res else 0

def place_demo_bet(account_id, betslip, config=DEFAULTS):
    acc = get_account(account_id)
    if not acc:
        raise Exception("account not found")
    if betslip['prob'] < config['min_confidence_for_bet']:
        return {"status":"skipped", "reason":"low_confidence"}
    placed = count_today_bets(acc['type'], betslip.get('market_type','multiple'))
    max_allowed = config['max_daily_multiples'] if betslip.get('market_type','multiple')=='multiple' else config['max_daily_singles']
    if placed >= max_allowed:
        return {"status":"skipped","reason":"daily_limit_reached"}
    bank = float(acc['balance'])
    stake = max(1.0, round(bank * config['fraction_of_bank_per_bet'], 2))
    cur = cursor()
    cur.execute("""INSERT INTO betslips (created_at, bets, totalOdd, stake, potentialReturn, status, account_type, market_type)
                   VALUES (now(), %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (json.dumps(betslip['selections']), betslip['combined_odd'], stake, stake*betslip['combined_odd'], 'pending', acc['type'], betslip.get('market_type','multiple')))
    res = cur.fetchone()
    cur.connection.commit()
    bet_id = res['id']
    adjust_balance(account_id, -stake)
    save_justification(bet_id, betslip.get('justification', {}))
    return {"status":"placed","bet_id":bet_id,"stake":stake}
