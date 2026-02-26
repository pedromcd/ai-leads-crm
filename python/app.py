from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import os
import sqlite3
import uuid
from typing import Optional

DB_PATH = os.getenv("DB_PATH", "../data/leads.db")

app = FastAPI()


class Lead(BaseModel):
    name: str
    email: Optional[str] = ""
    phone: Optional[str] = ""
    source: Optional[str] = "web"
    message: str
    intent: str
    priority: str
    score: int
    next_action: str
    suggested_reply: str


def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            source TEXT,
            message TEXT NOT NULL,
            intent TEXT NOT NULL,
            priority TEXT NOT NULL,
            score INTEGER NOT NULL,
            next_action TEXT NOT NULL,
            suggested_reply TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'NEW'
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


@app.get("/health")
def health():
    return {"ok": True, "db": DB_PATH}


@app.post("/lead")
def save_lead(lead: Lead):
    lead_id = str(uuid.uuid4())[:8]
    created_at = datetime.now().isoformat(timespec="seconds")

    # Garantias mínimas
    score = int(lead.score)
    if score < 0:
        score = 0
    if score > 100:
        score = 100

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO leads (
            id, created_at, name, email, phone, source, message,
            intent, priority, score, next_action, suggested_reply, status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'NEW')
        """,
        (
            lead_id,
            created_at,
            lead.name,
            lead.email or "",
            lead.phone or "",
            lead.source or "web",
            lead.message,
            lead.intent,
            lead.priority,
            score,
            lead.next_action,
            lead.suggested_reply,
        ),
    )
    conn.commit()
    conn.close()

    return {"ok": True, "lead_id": lead_id}


@app.get("/leads")
def list_leads(limit: int = 50):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM leads ORDER BY created_at DESC LIMIT ?",
        (limit,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"count": len(rows), "items": rows}