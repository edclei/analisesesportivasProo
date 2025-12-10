# ============================
# services/demo_engine.py
# ============================

import os
from datetime import datetime, timedelta
from supabase import create_client

# -------- SUPABASE INIT -------- #
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ======================= PLACE DEMO BET =======================
def place_demo_bet(account_id: str, payload: dict):

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
        return {"status": "DEMO BET OK", "bet": bet}
    except Exception as e:
        return {"error": str(e), "payload": bet}


# ======================= CLEANUP AUTO (OPCIONAL) =======================
def cleanup_old_demo():
    limit = datetime.utcnow() - timedelta(hours=24)
    supabase.table("demo_bets").delete().lt("timestamp", limit.isoformat()).execute()
    return {"cleanup": True}


