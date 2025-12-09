
# odds_adapter: normalize odds feed into a simple dict
def normalize_odds(raw):
    # raw: may be list or dict; return dict with 'home','draw','away' and 'movement'
    if isinstance(raw, dict):
        return {
            "home": raw.get("home") or raw.get('1') or raw.get('home_price'),
            "draw": raw.get("draw") or raw.get('x'),
            "away": raw.get("away") or raw.get('2') or raw.get('away_price'),
            "movement": raw.get("movement", 0)
        }
    return {"home": None, "draw": None, "away": None, "movement": 0}
