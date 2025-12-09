import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")

_conn = None

def get_conn():
    global _conn
    if _conn is None:
        if not DATABASE_URL:
            raise Exception("DATABASE_URL not set in env")
        _conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return _conn

def cursor():
    return get_conn().cursor()
