"""Enhanced demo engine for AnalisesEsportivasPro

Generates realistic simulated predictions using historical-like randomness,
predefined scenarios and configurable parameters.
"""
import random
import math
from datetime import datetime, timedelta

DEFAULT_MARKETS = [
    "MATCH_ODDS",
    "OVER_2.5",
    "UNDER_2.5",
    "BOTH_TEAMS_TO_SCORE"
]

def _random_prob(base=0.65, vol=0.12):
    # gaussian around base with clipping
    p = random.gauss(base, vol)
    return max(0.5, min(0.98, round(p, 2)))

def _simulate_odds_from_prob(p):
    # convert probability to decimal odds with a small house margin
    if p <= 0: p = 0.01
    margin = 0.04
    odds = (1.0 / p) * (1 + margin)
    return round(max(1.01, odds), 2)

def simulate_prediction(event=None, seed=None, market=None):
    """Return a simulated prediction dict for an event.
    event: optional dict with teams, time, competition.
    seed: optional int to reproduce.
    market: choose market or random.
    """
    if seed is not None:
        random.seed(seed)

    # build base event info
    now = datetime.utcnow()
    if event is None:
        event = {
            "home": "Time A",
            "away": "Time B",
            "kickoff": (now + timedelta(hours=random.randint(1,72))).isoformat()
        }

    market = market or random.choice(DEFAULT_MARKETS)
    # base probability depends on market
    if market == "MATCH_ODDS":
        base = random.choice([0.55, 0.60, 0.65, 0.70])
    elif market == "OVER_2.5":
        base = random.choice([0.52, 0.58, 0.63])
    elif market == "UNDER_2.5":
        base = random.choice([0.50, 0.57, 0.62])
    elif market == "BOTH_TEAMS_TO_SCORE":
        base = random.choice([0.53, 0.59, 0.66])
    else:
        base = 0.60

    prob = _random_prob(base=base, vol=0.10)
    odd = _simulate_odds_from_prob(prob)

    # add some confidence score and reason text
    conf = round(min(0.99, prob + random.uniform(-0.05, 0.08)), 2)
    reason_samples = [
        "Forma recente favorável",
        "Lesões no time adversário",
        "Vantagem em casa",
        "Tendência de gols",
        "Confronto direto histórico"
    ]
    reason = random.choice(reason_samples)

    return {
        "event": event,
        "market": market,
        "probability": prob,
        "recommended_odd": odd,
        "confidence": conf,
        "reason": reason,
        "generated_at": datetime.utcnow().isoformat()
    }

# convenience: generate a list of simulated entries
def simulate_batch(n=10):
    out = []
    for i in range(n):
        out.append(simulate_prediction())
    return out