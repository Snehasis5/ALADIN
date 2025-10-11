# evaluation_receiver.py
"""
Instructor-side endpoint to receive student repo callbacks (repo_url, commit_sha, pages_url)
Stores them in a SQLite DB for later evaluation.
"""

import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime

DB_PATH = os.getenv("REPOS_DB", "repos.db")
app = FastAPI(title="Evaluation Receiver")

# Ensure DB
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS repos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        email TEXT,
        task TEXT,
        round INTEGER,
        nonce TEXT,
        repo_url TEXT,
        commit_sha TEXT,
        pages_url TEXT
    )""")
    conn.commit()
    conn.close()

init_db()

class RepoPayload(BaseModel):
    email: str
    task: str
    round: int
    nonce: str
    repo_url: str
    commit_sha: str
    pages_url: str

@app.post("/repo-callback")
async def receive_repo(p: RepoPayload):
    # Validate: in a full implementation you would validate the task exists and nonce matches recorded tasks table.
    # For now we accept and store
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO repos (timestamp,email,task,round,nonce,repo_url,commit_sha,pages_url) VALUES (?,?,?,?,?,?,?,?)",
              (datetime.utcnow().isoformat(), p.email, p.task, p.round, p.nonce, p.repo_url, p.commit_sha, p.pages_url))
    conn.commit()
    conn.close()
    return {"status": "stored"}
