
import sqlite3, threading, json
from datetime import datetime
DB_PATH = "backend/demo/demo_demo.db"
_lock = threading.Lock()

def _get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with _lock:
        c = _get_conn(); cur = c.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS demo_bets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            match_id TEXT,
            teams TEXT,
            market TEXT,
            bet_type TEXT,
            selections TEXT,
            stake REAL,
            odds REAL,
            probability REAL,
            confidence REAL,
            justification TEXT,
            status TEXT,
            settled_at TEXT
        )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS demo_state (key TEXT PRIMARY KEY, value TEXT)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS daily_counters (day TEXT PRIMARY KEY, singles INTEGER DEFAULT 0, multis INTEGER DEFAULT 0, consecutive_losses INTEGER DEFAULT 0)""")
        c.commit()

def save_bet(bet):
    with _lock:
        c = _get_conn(); cur = c.cursor()
        cur.execute("""INSERT INTO demo_bets(created_at, match_id, teams, market, bet_type, selections, stake, odds, probability, confidence, justification, status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", (
            datetime.utcnow().isoformat(), bet.get('match_id'), bet.get('teams'), bet.get('market'), bet.get('bet_type'),
            bet.get('selections_json') or json.dumps(bet.get('selections') or {}), bet.get('stake'), bet.get('odds'),
            bet.get('probability'), bet.get('confidence'), bet.get('justification'), 'open'
        ))
        c.commit()
        return cur.lastrowid

def settle_bet(bet_id, result):
    with _lock:
        c = _get_conn(); cur = c.cursor()
        cur.execute("UPDATE demo_bets SET status=?, settled_at=? WHERE id=?", (result, datetime.utcnow().isoformat(), bet_id))
        c.commit()

def list_bets(limit=100):
    c = _get_conn(); cur = c.cursor()
    cur.execute("SELECT * FROM demo_bets ORDER BY created_at DESC LIMIT ?", (limit,))
    return [dict(r) for r in cur.fetchall()]

def get_daily_counters(day=None):
    if day is None:
        from datetime import datetime
        day = datetime.utcnow().date().isoformat()
    c = _get_conn(); cur = c.cursor()
    cur.execute("SELECT * FROM daily_counters WHERE day=?", (day,))
    r = cur.fetchone()
    if r:
        return dict(r)
    cur.execute("INSERT OR REPLACE INTO daily_counters(day, singles, multis, consecutive_losses) VALUES (?,0,0,0)", (day,))
    c.commit()
    return {'day': day, 'singles':0, 'multis':0, 'consecutive_losses':0}

def inc_counter(kind, amount=1):
    day = __import__('datetime').datetime.utcnow().date().isoformat()
    with _lock:
        c = _get_conn(); cur = c.cursor()
        get_daily_counters(day)
        if kind=='singles':
            cur.execute("UPDATE daily_counters SET singles = singles + ? WHERE day=?", (amount, day))
        else:
            cur.execute("UPDATE daily_counters SET multis = multis + ? WHERE day=?", (amount, day))
        c.commit()

def reset_daily_counters():
    day = __import__('datetime').datetime.utcnow().date().isoformat()
    with _lock:
        c = _get_conn(); cur = c.cursor()
        cur.execute("INSERT OR REPLACE INTO daily_counters(day, singles, multis, consecutive_losses) VALUES (?,0,0,0)", (day,))
        c.commit()

def inc_consecutive_losses(delta=1):
    day = __import__('datetime').datetime.utcnow().date().isoformat()
    with _lock:
        c = _get_conn(); cur = c.cursor()
        get_daily_counters(day)
        cur.execute("UPDATE daily_counters SET consecutive_losses = consecutive_losses + ? WHERE day=?", (delta, day))
        c.commit()

def set_setting(key, value):
    with _lock:
        c = _get_conn(); cur = c.cursor()
        cur.execute("INSERT OR REPLACE INTO demo_state(key,value) VALUES (?,?)", (key, str(value)))
        c.commit()

def get_setting(key, default=None):
    c = _get_conn(); cur = c.cursor()
    cur.execute("SELECT value FROM demo_state WHERE key=?", (key,))
    r = cur.fetchone()
    return r['value'] if r else default

init_db()
