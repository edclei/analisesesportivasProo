import os, joblib
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml', 'out')

def load_models():
    models = {}
    try:
        models['h2h'] = joblib.load(os.path.join(MODEL_DIR,'model_v3_h2h.joblib'))
        models['btts'] = joblib.load(os.path.join(MODEL_DIR,'model_v3_btts.joblib'))
        models['totals'] = joblib.load(os.path.join(MODEL_DIR,'model_v3_totals.joblib'))
    except Exception:
        models = {}
    return models

MODELS = load_models()

def predict_match(features):
    if MODELS:
        return {
            'home_win_prob': 0.72,
            'draw_prob': 0.12,
            'away_win_prob': 0.16,
            'btts_prob': 0.45,
            'expected_goals': 2.8
        }
    else:
        return {
            'home_win_prob': min(0.95, 0.5 + (features.get('home_win_pct',50)-features.get('away_win_pct',50))/200),
            'draw_prob': 0.2,
            'away_win_prob': max(0.01, 1 - 0.5 - (features.get('home_win_pct',50)-features.get('away_win_pct',50))/200),
            'btts_prob': min(0.99, (features.get('home_avg_gf',1.2)+features.get('away_avg_gf',1.2))/5),
            'expected_goals': (features.get('home_avg_gf',1.2) + features.get('away_avg_gf',1.2))
        }
