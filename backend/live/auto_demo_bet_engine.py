
from backend.live.detection_rules import aggregate_signals
from backend.betbuilder.betbuilder_v2 import build_ticket_from_teams
from backend.demo.demo_bet_engine import place_auto_demo
from backend.demo.demo_storage import get_setting
from datetime import datetime

def handle_match_check(match_data, profiles=None):
    agg = aggregate_signals(match_data, profiles=profiles)
    combined_score = agg['combined_score']; strong = agg['strong_detected']; markets = agg['markets']; justification = agg['justification']
    if not strong and combined_score < 0.80:
        return {'placed': False, 'reason': 'no_strong_pattern', 'score': combined_score}
    teams = [ match_data.get('home'), match_data.get('away') ] if match_data.get('home') else [match_data.get('home')]
    ticket = build_ticket_from_teams(teams, markets_per_team=min(3, len(markets)))
    ticket['created_at'] = datetime.utcnow().isoformat(); ticket['justification_auto'] = justification
    threshold = float(get_setting('confidence_threshold','0.8'))
    if ticket['confidence'] >= threshold:
        settings = {
            'confidence_threshold': get_setting('confidence_threshold','0.8'),
            'stake_pct_of_bank': float(get_setting('stake_pct_of_bank','0.02')),
            'max_multis_per_day': int(get_setting('max_multis_per_day','4')),
            'max_singles_per_day': int(get_setting('max_singles_per_day','4')),
            'allow_after_two_losses': get_setting('allow_after_two_losses','False') in ('True','true','1')
        }
        res = place_auto_demo(teams, settings)
        return {'placed': True, 'ticket': ticket, 'place_res': res}
    else:
        return {'placed': False, 'reason': 'confidence_below_threshold', 'confidence': ticket['confidence']}
