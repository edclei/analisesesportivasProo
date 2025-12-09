from fastapi import APIRouter, Query
from backend.services import demo_engine
from fastapi import HTTPException
from typing import Optional

router = APIRouter()

@router.get("/predict")
def predict(mode: Optional[str] = Query("real"), market: Optional[str] = Query(None), seed: Optional[int]=None):
    """Predict endpoint that supports demo mode.
    mode: 'demo' or 'real'. In 'demo' mode, uses demo_engine.simulate_prediction.
    """
    if mode == "demo":
        try:
            pred = demo_engine.simulate_prediction(market=market, seed=seed)
            return {"mode":"demo", "prediction": pred}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        # In real mode, delegate to existing predict if available
        # try to import existing predict function from backend.predictor or main
        try:
            from backend import main
            # if main has a function `predict_real` we call it (best-effort)
            if hasattr(main, "predict_real"):
                return {"mode":"real", "prediction": main.predict_real()}
            else:
                # fallback message
                return {"mode":"real", "prediction": "real model not configured in this demo"}
        except Exception:
            return {"mode":"real", "prediction": "real model not available"}