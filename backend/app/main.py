import os
import json
from fastapi import FastAPI
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = FastAPI()

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
