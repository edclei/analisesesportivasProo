
from fastapi import APIRouter
from backend.demo.demo_storage import list_bets, get_daily_counters
from backend.live.detection_rules import aggregate_signals
router = APIRouter(prefix="/live")

@router.get("/tickets")
def tickets(limit: int = 100):
    return list_bets(limit)

@router.get("/signals")
def signals():
    # For demo, run a lightweight scan over today's matches (calls local endpoint)
    try:
        import requests, datetime
        r = requests.get("http://localhost:8000/api/sportmonks/matches/today", timeout=5)
        data = r.json() if r.status_code==200 else []
    except Exception:
        data = []
    out = []
    for m in (data.get('data') if isinstance(data, dict) else data):
        md = {
            "match_id": m.get("id"),
            "home": m.get("home_team", m.get("home")),
            "away": m.get("away_team", m.get("away")),
            "kickoff": m.get("kickoff", m.get("starting_at")),
            "stats": m.get("stats", {}),
            "odds": m.get("odds", {}),
            "live": m.get("live", {})
        }
        out.append(aggregate_signals(md))
    return out
