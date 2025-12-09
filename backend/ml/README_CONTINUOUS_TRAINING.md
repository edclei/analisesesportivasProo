
Continuous training added:
- backend/ml/online_trainer.py  -> trains RandomForest on settled demo bets
- backend/ml/train_utils.py    -> dataset builder and persistence
- backend/demo/jobs.py         -> now triggers periodic retrain (hourly and daily)
How it works:
- Settled demo bets from demo_storage (status 'won' or 'lost') are used to build X,y.
- Model saved to backend/registry/model_online.joblib
- To force retrain: call backend.ml.online_trainer.trigger_retrain()
Notes:
- Uses sklearn; ensure backend/requirements.txt includes scikit-learn and joblib
- For production, replace SQLite storage with a central DB (Supabase) and use MLflow for model registry
