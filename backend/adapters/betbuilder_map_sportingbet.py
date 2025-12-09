
# best-effort mapping to produce a Sportingbet search URL or information for manual placing.
def build_sporting_search_url(teams):
    base = 'https://www.sportingbet.bet.br/pt-br/sports'
    q = '+'.join([t.replace(' ', '+') for t in teams if t])
    return f"{base}?q={q}"
