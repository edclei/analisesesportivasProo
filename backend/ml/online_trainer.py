
"""Online trainer for AnalisesEsportivasPro
- builds training dataset from demo storage (settled bets)
- trains a RandomForestClassifier to predict bet win/loss
- saves model to backend/registry/model_online.joblib
- exposes trigger_retrain() to be called by jobs or after settle
"""
import os, json, joblib
from datetime import datetime
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from backend.demo.demo_storage import _get_conn
from backend.ml.train_utils import build_dataset_from_db, persist_model, model_path, load_model_if_exists

def train_and_save(min_samples=20):
    X, y = build_dataset_from_db()
    if len(y) < min_samples:
        print(f"Not enough samples to train (have {len(y)}, need {min_samples})")
        return {"trained": False, "reason": "not_enough_samples", "n": len(y)}
    X = np.array(X)
    y = np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = float(accuracy_score(y_test, preds))
    prec = float(precision_score(y_test, preds, zero_division=0))
    rec = float(recall_score(y_test, preds, zero_division=0))
    persist_model(model)
    metrics = {"accuracy": acc, "precision": prec, "recall": rec, "trained_at": datetime.utcnow().isoformat(), "n_samples": len(y)}
    print("Trained model metrics:", metrics)
    return {"trained": True, "metrics": metrics}

def trigger_retrain(min_samples=20):
    return train_and_save(min_samples=min_samples)

if __name__ == "__main__":
    print(trigger_retrain())
