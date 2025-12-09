
# sportmonks_adapter: simple wrapper to normalize sportmonks responses
def normalize_fixture(raw):
    # raw expected to be a dict from SportMonks-like API
    return {
        "id": raw.get("id"),
        "home": raw.get("home") or raw.get("home_team") or raw.get("home_name"),
        "away": raw.get("away") or raw.get("away_team") or raw.get("away_name"),
        "kickoff": raw.get("kickoff") or raw.get("starting_at"),
        "stats": raw.get("stats", {}),
        "odds": raw.get("odds", {}),
        "live": raw.get("live", {})
    }
