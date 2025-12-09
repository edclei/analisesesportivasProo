
from fastapi_utils.tasks import repeat_every
from datetime import datetime, timedelta
from backend.live.auto_demo_bet_engine import handle_match_check
from backend.demo.demo_storage import list_bets
import logging, time

log = logging.getLogger('live_watchdog')

def fetch_matches_window():
    # For RUNNING in this environment we will not call external API.
    # Instead, this function should be replaced by a proper adapter in production.
    return []

@repeat_every(seconds=15)
def scan_and_place():
    log.info('Live watchdog scanning matches... (placeholder)')
    matches = fetch_matches_window()
    for m in matches:
        res = handle_match_check(m, profiles=['A','B','C','D'])
        log.info('scan result: %s', res)
