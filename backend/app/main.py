import os
import json
import sqlite3
import re
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = FastAPI()

DB_PATH = "/app/db/guestbook.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS guestbook (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


init_db()


class GuestbookEntry(BaseModel):
    name: str
    email: str
    message: str

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SPREADSHEET_ID = "1Gzz_izN9s7-aQIaArdFJrDcAH_Woj6oHDVqh4RLSFcs"
SHEET_RANGE = "Dinners 2026!A2:B"  # Skip header row


def get_sheets_service():
    creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if creds_json:
        info = json.loads(creds_json)
        creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    else:
        creds_path = os.environ.get("GOOGLE_CREDENTIALS_PATH", "/app/credentials/service-account.json")
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello hello from raspberry pi"}


@app.get("/api/guestbook")
def get_guestbook():
    conn = get_db()
    rows = conn.execute(
        "SELECT name, message, created_at FROM guestbook ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.post("/api/guestbook", status_code=201)
def post_guestbook(entry: GuestbookEntry):
    name = entry.name.strip()
    email = entry.email.strip()
    message = entry.message.strip()

    if not name or len(name) > 100:
        raise HTTPException(status_code=422, detail="Name is required (max 100 chars)")
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        raise HTTPException(status_code=422, detail="Invalid email address")
    if not message:
        raise HTTPException(status_code=422, detail="Message is required")
    word_count = len(message.split())
    if word_count > 100:
        raise HTTPException(status_code=422, detail=f"Message too long ({word_count} words, max 100)")

    conn = get_db()
    conn.execute(
        "INSERT INTO guestbook (name, email, message, created_at) VALUES (?, ?, ?, ?)",
        (name, email, message, datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}


@app.get("/api/dinners")
def dinners():
    service = get_sheets_service()
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range=SHEET_RANGE)
        .execute()
    )
    rows = result.get("values", [])
    data = []
    for row in rows:
        if len(row) >= 2:
            try:
                count = int(row[0])
            except (ValueError, IndexError):
                continue
            data.append({"count": count, "dish": row[1]})
    return data
