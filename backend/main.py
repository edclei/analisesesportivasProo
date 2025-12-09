from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os, json
from services.accounts import create_account, get_account
from backend.services.demo_engine import place_demo_bet
import sys
sys.path.append(".")
from services.demo_engine import place_demo_bet
from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health():
    return {"status": "online", "app": "AnalisesEsportivasPro"}



load_dotenv()  


app = FastAPI(title="Sports Analyzer API")

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
def api_place_demo_br(req: BetRequest):
    if req.prob < 0 or req.prob > 1:
        raise HTTPException(status_code=400, detail="prob invalid")
    result = place_demo_bet(req.account_id, {
        "selections": req.selections,
        "combined_odd": req.combined_odd,
        "prob": req.prob,
        "market_type": req.market_type,
        "justification": req.justification
    })
    return result

@app.get("/api/health")
def health():
    return {"status":"ok","service":"sports-analyzer"}


# Added demo predict router
from backend.routes import predict_demo
app.include_router(predict_demo.router)


# include betbuilder router
from backend.routes import betbuilder
app.include_router(betbuilder.router)



# --- Activation additions: ensure demo jobs, live watchdog and routers are registered ---
try:
    import backend.demo.jobs  # registers periodic jobs (trainer, maintenance)
except Exception as e:
    print("Could not import backend.demo.jobs:", e)

try:
    import backend.live.live_watchdog  # starts live watchdog repeat_every tasks
except Exception as e:
    print("Could not import backend.live.live_watchdog:", e)

# include demo API router if available
try:
    from backend.demo import api as demo_api
    app.include_router(demo_api.router)
except Exception as e:
    print("demo.api not available:", e)

# include betbuilder router if available
try:
    from backend.routes import betbuilder as betbuilder_router
    app.include_router(betbuilder_router.router)
except Exception as e:
    print("betbuilder router not available:", e)

# include live routes if present
try:
    from backend.routes import live as live_router
    app.include_router(live_router.router)
except Exception as e:
    print("live router not available:", e)
