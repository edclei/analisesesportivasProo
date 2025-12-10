from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os, json, sys

# Garantir que serviço backend seja enxergado
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#  IMPORTAÇÃO CORRETA
from services.demo_engine import place_demo_bet
from services.accounts import create_account, get_account

load_dotenv()

app = FastAPI(title="Analises Esportivas PRO API")


# ---------------- HEALTHCHECK ----------------

@app.get("/api/health")
def health():
    return {"status": "online", "service": "AnalisesEsportivasPro", "demo_engine": "ACTIVE"}



# ---------------- CRIAÇÃO DE CONTA ----------------

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
    if req.prob < 0 or req.prob > 1:
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



# ---------------- ROTAS EXTRAS (CARREGAMENTO SEGURO) ----------------

# Demo predictions
try:
    from backend.routes import predict_demo
    app.include_router(predict_demo.router)
except:
    print("⚠ predict_demo router nao encontrado")

# Betbuilder dynamic bets
try:
    from backend.routes import betbuilder
    app.include_router(betbuilder.router)
except:
    print("⚠ betbuilder router nao encontrado")

# Demo jobs automáticos
try:
    import backend.demo.jobs
except Exception as e:
    print("⚠ demo jobs nao carregado:", e)

# Live Watchdog
try:
    import backend.live.live_watchdog
except Exception as e:
    print("⚠ live watchdog nao carregado:", e)

# Live routes
try:
    from backend.routes import live as live_router
    app.include_router(live_router.router)
except:
    print("⚠ live router nao encontrado")


