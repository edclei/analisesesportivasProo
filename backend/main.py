from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, sys
from dotenv import load_dotenv

# garante path correto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# IMPORTAÇÃO CORRETA
from services.demo_engine import place_demo_bet
from services.accounts import create_account, get_account

app = FastAPI(title="Sports Analyzer API")

load_dotenv()

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "sports-analyzer"}

class CreateAccountPayload(BaseModel):
    user_id: str
    account_type: str
    initial_balance: float = 1000.0

@app.post("/api/account/create")
def api_create_account(payload: CreateAccountPayload):
    if payload.account_type not in ('demo','real'):
        raise HTTPException(status_code=400, detail="invalid type")
    acc = create_account(payload.user_id, f"{payload.account_type}_account", payload.account_type, payload.initial_balance)
    return {"status":"ok","account":acc}

class BetRequest(BaseModel):
    account_id: str
    selections: list
    combined_odd: float
    prob: float
    market_type: str = 'multiple'
    justification: dict = {}

@app.post("/api/bet/place_demo")
def api_place_demo(req: BetRequest):
    result = place_demo_bet(req.account_id, {
        "selections": req.selections,
        "combined_odd": req.combined_odd,
        "prob": req.prob,
        "market_type": req.market_type,
        "justification": req.justification
    })
    return result

# Rotas adicionais
try:
    from backend.routes import predict_demo, betbuilder
    app.include_router(predict_demo.router)
    app.include_router(betbuilder.router)
except:
    print("Routes não carregadas — verificar paths")


