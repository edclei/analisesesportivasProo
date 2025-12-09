
# backend/routes/betbuilder.py
from fastapi import APIRouter, Body, HTTPException
from typing import List, Dict, Any
from backend.betbuilder.betbuilder_v2 import build_ticket_from_teams, ticket_edit_apply
from backend.demo.demo_storage import save_bet, list_bets, get_setting, set_setting

router = APIRouter(prefix="/betbuilder")

@router.post('/create')
def create_ticket(payload: Dict[str,Any] = Body(...)):
    teams = payload.get('teams') or []
    markets_per_team = int(payload.get('markets_per_team', 2))
    max_teams = int(payload.get('max_teams', 10))
    if not teams:
        raise HTTPException(status_code=400, detail='teams required')
    ticket = build_ticket_from_teams(teams, markets_per_team=markets_per_team, max_teams=max_teams)
    # return ticket for review (not placing as demo bet automatically)
    return ticket

@router.post('/apply_edits')
def apply_edits(payload: Dict[str,Any] = Body(...)):
    ticket = payload.get('ticket')
    edits = payload.get('edits', {})
    if not ticket:
        raise HTTPException(status_code=400, detail='ticket required')
    new_ticket = ticket_edit_apply(ticket, edits)
    return new_ticket

@router.get('/redirect_url')
def redirect_url(ticket_id: str, ticket_json: str = None):
    # Attempt to build a Sportingbet URL for the ticket. Since Sportingbet does not provide a public deep-link spec,
    # we create a best-effort search URL that opens the sports page and includes a query of team names.
    base = 'https://www.sportingbet.bet.br/pt-br/sports'
    # if ticket_json provided (URL-encoded), try to decode teams
    if ticket_json:
        try:
            import urllib.parse as up
            obj = up.loads(ticket_json)
            teams = []
            for m in obj.get('matches', []):
                teams.append(m.get('team'))
            q = '+'.join([t.replace(' ', '+') for t in teams if t])
            return { 'url': f"{base}?q={q}" }
        except Exception:
            pass
    # fallback with ticket_id only
    return { 'url': base }
