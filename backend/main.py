import time
time.sleep(10)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

# ✅ ADD THIS BLOCK (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = psycopg2.connect(
 host="postgres",
    database="logsdb",
    user="admin",
    password="admin"
)

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/logs")
def get_logs():
    cur = conn.cursor()
    cur.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50")
    return cur.fetchall()

@app.get("/stats")
def stats():
    cur = conn.cursor()
    cur.execute("SELECT level, COUNT(*) FROM logs GROUP BY level")
    return cur.fetchall()
