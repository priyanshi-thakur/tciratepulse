import sqlite3, json
from .config import DB_PATH

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute('''CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT NOT NULL, expires_at INTEGER NOT NULL)''')
        con.execute('''CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY, created_at TEXT DEFAULT CURRENT_TIMESTAMP, request TEXT, response TEXT)''')

def get_cache(key):
    import time
    with sqlite3.connect(DB_PATH) as con:
        row = con.execute("SELECT value FROM cache WHERE key=? AND expires_at>?", (key, int(time.time()))).fetchone()
    return json.loads(row[0]) if row else None

def set_cache(key, value, seconds=21600):
    import time
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT OR REPLACE INTO cache VALUES(?,?,?)", (key, json.dumps(value), int(time.time())+seconds))

def save_quote(req, res):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT INTO quotes(request,response) VALUES (?,?)", (json.dumps(req),json.dumps(res)))
