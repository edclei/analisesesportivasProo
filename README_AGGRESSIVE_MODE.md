
AGGRESSIVE OMEGA MODE (3)
-------------------------
This distribution configures the system to run in Aggressive Omega mode:
- Higher staking using a hybrid Kelly + confidence multiplier (see core/strategy.py)
- More markets per team by default
- AUTO demo placing enabled for rapid learning
- Live polling every 15 seconds (configurable in core/config_aggressive.json)

Files added/updated:
- core/config_aggressive.json
- core/markets.py (50 markets)
- core/strategy.py (aggressive staking)
- Procfile and start.sh use ${PORT:-8000}

Use with caution: aggressive staking increases volatility. Recommended for demo account only.
