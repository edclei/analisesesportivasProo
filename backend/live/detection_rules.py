
from datetime import datetime
def rule_goals_pressure(match_data):
    stats = match_data.get('stats',{})
    xg_home = stats.get('xg_home', 0); xg_away = stats.get('xg_away',0)
    attacks = stats.get('attacks', 0)
    score = min(0.99, (xg_home + xg_away) / 2.0 / 0.6)
    triggered = score > 0.6
    reason = f"xG combined {xg_home + xg_away:.2f}, attacks {attacks}"
    return {'signal': triggered, 'score': round(score,3), 'reason': reason, 'market':'OVER_GOALS'}

def rule_corners_rush(match_data):
    live = match_data.get('live', {})
    last_10_min_corners = live.get('corners_10m', 0)
    avg = match_data.get('stats', {}).get('avg_corners', 5.0)
    score = min(0.99, (last_10_min_corners / max(1.0, avg/3.0)))
    triggered = score > 0.8
    reason = f"corners 10m {last_10_min_corners}, avg {avg}"
    return {'signal': triggered, 'score': round(score,3), 'reason': reason, 'market':'OVER_CORNERS'}

def rule_cards_aggression(match_data):
    live = match_data.get('live', {})
    last_cards = live.get('cards_15m', 0)
    recent_fouls = live.get('fouls_15m', 0)
    score = min(0.99, (last_cards * 0.3 + recent_fouls * 0.05))
    triggered = score > 0.6
    reason = f"cards15 {last_cards}, fouls15 {recent_fouls}"
    return {'signal': triggered, 'score': round(score,3), 'reason': reason, 'market':'OVER_CARDS'}

def rule_result_value(match_data):
    odds = match_data.get('odds', {})
    home_odd = odds.get('home') or odds.get('1') or 1.01
    movement = odds.get('movement', 0)
    score = max(0.0, 0.5 - movement*0.1 + 0.3)
    triggered = score > 0.75
    reason = f"home_odd {home_odd}, movement {movement}"
    return {'signal': triggered, 'score': round(score,3), 'reason': reason, 'market':'1X2'}

def aggregate_signals(match_data, profiles=None):
    rules = {'A': rule_goals_pressure, 'B': rule_corners_rush, 'C': rule_result_value, 'D': rule_cards_aggression}
    if profiles is None: profiles = ['A','B','C','D']
    results = []
    for p in profiles:
        r = rules.get(p, lambda m: {'signal': False, 'score':0, 'reason':'na', 'market':'NA'})(match_data)
        results.append(r)
    scores = [r['score'] for r in results]
    combined = sum(scores)/len(scores) if scores else 0.0
    strong = any(r['score'] >= 0.8 for r in results)
    markets = [r['market'] for r in sorted(results, key=lambda x: x['score'], reverse=True) if r['score']>0.45][:4]
    justification = '; '.join([f"{r['market']}({r['score']}):{r['reason']}" for r in results])
    return {'combined_score': round(combined,3), 'strong_detected': strong, 'markets': markets, 'justification': justification}
