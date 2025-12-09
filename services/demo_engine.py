import time
import json
from datetime import datetime, timedelta
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ------------------- IA APOSTAS DEMO / ABCDE AUTO ENGINE -------------------

def place_demo_bet(match_id: str, stake: float, markets: list, confidence: float):
    """
    Simula aposta demo usando o motor FULL AUTO ABCDE
    """

    bet = {
        "match_id": match_id,
        "stake": stake,
        "markets": markets,
        "confidence": confidence,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "pending"  # resultado será atualizado após o jogo
    }

    supabase.table("bets_demo").insert(bet).execute()

    return {
        "msg": "APOSTA DEMO REGISTRADA ✔",
        "demo_mode": "ACTIVE FULL AUTO",
        "confidence": confidence,
        "stake_usada": stake,
        "markets": markets,
        "match": match_id
    }



# ------------------- IA MONTA BILHETES AUTOMÁTICOS -------------------

def ai_generate_ticket(matches_data: list):
    """
    IA analisa padrões e gera múltiplas automaticamente
    """

    ticket = []
    for game in matches_data:

        patterns = []

        if game["gols_média"] > 1.2:
            patterns.append("Mais de 0.5 Gols")

        if game["cartoes_media"] > 3:
            patterns.append("Mais de 2.5 Cartões")

        if game["escanteios_média"] < 12:
            patterns.append("Menos de 11.5 escanteios")

        if game["win_prob_team1"] > 0.55:
            patterns.append(f"{game['time1']} vence")

        ticket.append({
            "match_id": game["id"],
            "mercados": patterns,
            "iacalc_conf": round((len(patterns) * 18), 2)  # confiança IA 0–100%
        })

    return {"bilhete_gerado": ticket}




# ------------------- LIMPEZA AUTOMÁTICA 24 HORAS -------------------

def cleanup_old_bets():
    limite = datetime.utcnow() - timedelta(hours=24)
    supabase.table("bets_demo").delete().lt("timestamp", limite.isoformat()).execute()
    return "Limpeza concluída 🧹"
