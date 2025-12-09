
# core/strategy.py
# Hybrid Kelly + Confidence aggressive staking
def compute_stake(bankroll, confidence, prob, odds, max_pct=0.1):
    """Return stake amount.
    - bankroll: total demo bank
    - confidence: model confidence 0-1
    - prob: model estimated probability 0-1
    - odds: offered decimal odds
    - max_pct: maximum fraction of bankroll per bet (aggressive default 10%)
    """
    # Kelly fraction (simplified): f* = (bp - q) / b where b = odds-1, q=1-p
    b = max(odds - 1.0, 0.0001)
    q = 1.0 - prob
    kelly = 0.0
    try:
        kelly = (b * prob - q) / b
    except Exception:
        kelly = 0.0
    # scale kelly by confidence (more confidence -> more of kelly)
    scaled_kelly = max(0.0, kelly * (0.5 + 0.5 * confidence))
    # hybrid: combine scaled_kelly with direct confidence multiplier
    conf_component = min(1.0, confidence * 0.5)
    raw_fraction = scaled_kelly + conf_component * 0.02  # small base from confidence
    # aggressive cap
    fraction = min(max_pct, max(0.001, raw_fraction * 3.0))  # amplify for aggressive mode
    return round(bankroll * fraction, 2)
