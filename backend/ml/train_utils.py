
"""Utilities for online training: dataset builder and model persistence"""
import os, json, joblib
from pathlib import Path
from backend.demo.demo_storage import _get_conn
from datetime import datetime

registry_dir = Path(__file__).parent.parent / 'backend' if False else Path(__file__).parent.parent / ''
# The actual model path inside project
model_path = Path(__file__).parent.parent.parent / 'backend' / 'registry' / 'model_online.joblib'
model_path.parent.mkdir(parents=True, exist_ok=True)

def build_dataset_from_db(limit=10000):
    """Read settled bets from demo_storage and construct feature matrix X and labels y.
    Features (example):
      - confidence, probability, odds, stake, bet_type (0 single,1 multi), hour_of_day
    Label:
      - win -> 1, lost -> 0
    """
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM demo_bets WHERE status IN ('won','lost') ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    X = []
    y = []
    for r in rows:
        try:
            confidence = float(r['confidence'] or 0.0)
            prob = float(r['probability'] or 0.0)
            odds = float(r['odds'] or 1.0)
            stake = float(r['stake'] or 0.0)
            bet_type = 1 if (r['bet_type'] and r['bet_type'].upper().startswith('MULTI')) else 0
            created = r['created_at']
            hour = 0
            try:
                hour = int(datetime.fromisoformat(created).hour)
            except Exception:
                hour = 0
            X.append([confidence, prob, odds, stake, bet_type, hour])
            y.append(1 if r['status'] == 'won' else 0)
        except Exception:
            continue
    return X, y

def persist_model(model):
    joblib.dump(model, model_path)
    print(f"Model persisted to {model_path}")

def load_model_if_exists():
    if model_path.exists():
        return joblib.load(model_path)
    return None
