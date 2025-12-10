from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os, json, sys

# PATH FIX
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# IMPORTAÇÃO CORRETA (SEM PARENTESES)
from services.demo_engine import place_demo_bet
from services.accounts import create_account, get_account

load_dotenv()

app = FastAPI(title="Analises Esportivas PRO API")


# ---------------- HEALTH ----------------
@app.get("/api/health")
def health():
    return {"status": "online", "service": "AnalisesEsportivasPro", "demo_engine": "ACTIVE"}



# ---------------- CONTA ----------------

class CreateAccountPayload(BaseModel):
    user_id: str
    account_type: str
    initial_balance: float = 1000.0

@app.post("/api/account/create")
def api_create_account(payload: CreateAccountPayload):
    if payload.account_type not in ('demo','real'):
        raise HTTPException(status_code=400, detail="invalid type")

    acc = create_account(
        payload.user_id,
        f"{payload.account_type}_account",
        payload.account_type,
        payload.initial_balance
    )
    return {"status": "ok", "account": acc}



# ---------------- APOSTA DEMO ----------------

class BetRequest(BaseModel):
    account_id: str
    selections: list
    combined_odd: float
    prob: float
    market_type: str = 'multiple'
    justification: dict = {}

@app.post("/api/bet/place_demo")
def api_place_demo(req: BetRequest):
    if not 0 <= req.prob <= 1:
        raise HTTPException(status_code=400, detail="prob invalid")

    result = place_demo_bet(
        req.account_id,
        {
            "selections": req.selections,
            "combined_odd": req.combined_odd,
            "prob": req.prob,
            "market_type": req.market_type,
            "justification": req.justification
        }
    )
    return result



# ROTAS EXTRAS (só carrega se existir)
def try_include(path, name):
    try:
        module = __import__(path, fromlist=[name])
        app.include_router(getattr(module, name).router)
        print(f"🔗 Router carregado: {name}")
    except:
        print(f"⚠ Router ignorado: {name}")

try_include("backend.routes.predict_demo", "predict_demo")
try_include("backend.routes.betbuilder", "betbuilder")
try_include("backend.routes.live", "live_router")

print("🚀 API carregada com sucesso")

