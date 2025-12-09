def place_demo_bet(match_id: str, stake: float, markets: list = None):
    return {
        "status": "demo-bet-placed",
        "match_id": match_id,
        "stake": stake,
        "markets_used": markets or []
    }
