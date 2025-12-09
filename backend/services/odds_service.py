import os, requests
from dotenv import load_dotenv
load_dotenv()
ODDS_KEY = os.getenv("ODDS_API_KEY","")
ODDS_BASE = "https://api.odds-api.io/v4"

def fetch_odds(sport='soccer_epl'):
    if not ODDS_KEY:
        raise Exception('ODDS_API_KEY not set in env')
    params = {"api_key": ODDS_KEY, "sport": sport, "region": "eu", "mkt":"h2h"}
    r = requests.get(f"{ODDS_BASE}/odds", params=params, timeout=20)
    r.raise_for_status()
    return r.json()
