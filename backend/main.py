# ============================
# main.py
# ============================
import sys, os
from fastapi import FastAPI, HTTPException
from backend.main import app  # certifica source único p/ uvicorn

from pydantic import BaseModel
from dotenv import load_dotenv

# Corrige PATH para reconhecer /services/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# -------- IMPORTAÇÕES CORRETAS -------- #
from services.demo_engine import place_demo_bet
from services.accounts import create_account, get_account

# -------- INICIALIZAÇÃO -------- #
load_dotenv()
app = FastAPI(title="Analises Esportivas Pro — API")


# ======================= HEALTH CHECK =======================
@app.get("/")
@app.get("/api/health")
def root():
    return {"status": "online", "project": "Analises Esportivas Pro"}


# ======================= CRIAR CONTA =======================
class CreateAccountPayload(BaseModel):
    user_id: str
    account_type: str  # demo / real
    initial_balance: float = 1000.0

@app.post("/api/account/create")
def account_create(payload: CreateAccountPayload):

    if payload.account_type not in ("demo", "real"):
        raise HTTPException(status_code=400, detail="tipo inválido")

    acc = create_account(
        payload.user_id,
        f"{payload.account_type}_account",
        payload.account_type,
        payload.initial_balance
    )

    return {"status": "ok", "account": acc}


# ======================= PLACE DEMO BET =======================
class BetRequest(BaseModel):
    account_id: str
    selections: list
    combined_odd: float
    prob: float
    market_type: str = "multiple"
    justification: dict = {}

@app.post("/api/bet/place_demo")
def bet_demo(req: BetRequest):

    if not (0 <= req.prob <= 1):
        raise HTTPException(status_code=400, detail="prob deve ser entre 0–1")

    return place_demo_bet(req.account_id, {
        "selections": req.selections,
        "combined_odd": req.combined_odd,
        "prob": req.prob,
        "market_type": req.market_type,
        "justification": req.justification
    })

