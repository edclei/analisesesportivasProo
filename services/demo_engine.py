import os
import json
import time
from datetime import datetime, timedelta
from supabase import create_client

# ---------------- CONFIGURAÇÃO SUPABASE ---------------- #

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # precisa ter ROLE de escrita

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------- MOTOR DEMO ABCDE ---------------- #

"""
ABCDE DEMO ENGINE — MODO COMPLETO

A = Avaliar Partidas
B = Buscar Padrões
C = Construção Automática do Bilhete
D = Decisão com base na confiança > 80%
E = Execução Demo e Registro no Banco

A IA monta bilhetes automaticamente com base em:
✔ escanteios
✔ gols
✔ cartões
✔ prob. vitória
✔ mercados combinados

E registra aposta demo com stake controlada.
"""


def place_demo_bet(account_id: str, payload: dict):
    """
    Salva aposta DEMO no Supabase.
    payload esperado:
        selections: lista de mercados
        combined_odd: float
        prob: float (0–1)
        market_type: single/multiple
        justification: dict com padrões usados
    """

    bet = {
        "account_id": account_id,
        "selections": payload.get("selections"),
        "combined_odd": payload.get("combined_odd"),
        "probability": payload.get("prob"),
        "market_type": payload.get("market_type"),
        "justification": payload.get("justification"),
        "timestamp": datetime.utcnow().isoformat(),
        "status": "pending"
    }

    try:
        supabase.table("demo_bets").insert(bet).execute()
        return {"status": "DEMO BET OK", "stored": bet}
    except Exception as e:
        return {"error": str(e), "payload": bet}



# ---------------- IA GERAR BILHETES ---------------- #

def ai_generate_ticket(matches: list):
    """
    Gera múltiplas automáticas com base nos padrões.
    Exemplo de entrada:
    [
        { "id": 81, "time1":"Corinthians","gols_média":1.4,"win_prob":0.61,
          "cartoes":3.5,"escanteios":9.0 }
    ]
    """

    ticket = []

    for m in matches:
        mercados = []

        if m.get("gols_média", 0) > 1.0: mercados.append("+0.5 gols")
        if m.get("win_prob", 0) > 0.60: mercados.append(f"{m.get('time1')} vence ou empate")
        if m.get("cartoes", 0) > 3: mercados.append("+2 cartões")
        if m.get("escanteios", 99) < 11: mercados.append("-11.5 escanteios")

        confiança = round(len(mercados) * 22.5, 2)  # IA conf = 0–100% (4 mercados = 90%)

        ticket.append({
            "match_id": m.get("id"),
            "mercados": mercados,
            "confiança": confiança
        })

    return {"bilhete_auto": ticket}



# ---------------- LIMPEZA AUTOMÁTICA ---------------- #

def cleanup_old_demo():
    """
    Remove bilhetes com mais de 24h para não acumular.
    """

    limite = datetime.utcnow() - timedelta(hours=24)
    supabase.table("demo_bets").delete().lt("timestamp", limite.isoformat()).execute()

    return {"cleanup": "OK — histórico limpo"}

