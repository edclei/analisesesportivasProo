# ================================
# MAIN API — FastAPI Server
# ================================

from fastapi import FastAPI
from datetime import datetime
from engine.abcde_engine import ai_generate_ticket, place_demo_bet, cleanup_old_demo

app = FastAPI(title="ABCDE BET ENGINE API")

@app.get("/")
def home():
    return {"status": "online", "msg": "API rodando com sucesso!"}

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow()}

@app.post("/generate")
def gerar_bilhetes(matches: list):
    return ai_generate_ticket(matches)

@app.post("/bet/demo")
def aposta_demo(account_id: str, payload: dict):
    return place_demo_bet(account_id, payload)

@app.delete("/cleanup")
def limpar():
    return cleanup_old_demo()
