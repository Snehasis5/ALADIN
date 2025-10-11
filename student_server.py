import os
import base64
import json
import shutil
import tempfile
import asyncio
import hashlib
from pathlib import Path
from typing import List, Optional
import traceback

import httpx
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from github_utils import create_or_upsert_github_repo_and_push, enable_github_pages
from generator import generate_project_from_brief
from config import GITHUB_TOKEN, GITHUB_OWNER, API_SECRET_MAP, KEEP_BUILD_ARTIFACTS

app = FastAPI(title="Student Task Receiver")

# --- Load Secrets ---
SECRET_MAP_PATH = API_SECRET_MAP
if Path(SECRET_MAP_PATH).exists():
    with open(SECRET_MAP_PATH, "r") as f:
        SECRET_MAP = json.load(f)
else:
    SECRET_MAP = {}

# --- Models ---
class Attachment(BaseModel):
    name: str
    url: str

class TaskRequest(BaseModel):
    email: str
    secret: str
    task: str
    round: int
    nonce: str
    brief: str
    checks: Optional[List[str]] = []
    evaluation_url: str
    attachments: Optional[List[Attachment]] = []

# --- Middleware for logging ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"➡️ {request.method} {request.url}")
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"❌ Exception during request: {e}")
        traceback.print_exc()
        raise e

# --- Global exception handler ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print("🔥 Global exception caught:\n", tb)
    return JSONResponse(status_code=500, content={"detail": str(exc)})

# --- Helpers ---
def verify_secret(email: str, secret: str):
    expected = SECRET_MAP.get(email)
    if expected is None:
        return not SECRET_MAP and bool(secret)
    return expected == secret

async def post_with_retries(url: str, json_payload: dict, max_attempts=6):
    attempt = 0
    async with httpx.AsyncClient(timeout=60) as client:
        while attempt < max_attempts:
            try:
                r = await client.post(url, json=json_payload)
                if r.status_code == 200:
                    return True
                print(f"[notify] attempt {attempt} failed: {r.status_code} {r.text}")
            except Exception as e:
                print(f"[notify] attempt {attempt} error: {e}")
            await asyncio.sleep(2 ** attempt)
            attempt += 1
    return False

async def is_org_account(owner: str) -> bool:
    if not owner:
        return False
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(f"https://api.github.com/users/{owner}")
        if r.status_code == 200:
            return r.json().get("type") == "Organization"
        return False

def slugify(s: str) -> str:
    import re
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60]

# --- API Endpoint ---
@app.post("/api-endpoint")
async def api_endpoint(req: TaskRequest):
    print(f"📥 Received task for {req.email} ({req.task})")

    if not verify_secret(req.email, req.secret):
        raise HTTPException(status_code=400, detail="Secret mismatch")

    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="Server misconfigured: missing GITHUB_TOKEN")

    tmp = Path(tempfile.mkdtemp(prefix="task-"))
    attachments_dir = tmp / "attachments"
    attachments_dir.mkdir(parents=True, exist_ok=True)

    # Save attachments
    for att in req.attachments or []:
        try:
            if att.url.startswith("data:"):
                _, b64 = att.url.split(",", 1)
                (attachments_dir / att.name).write_bytes(base64.b64decode(b64))
            else:
                r = httpx.get(att.url, timeout=20)
                r.raise_for_status()
                (attachments_dir / att.name).write_bytes(r.content)
            print(f"✅ Attachment saved: {att.name}")
        except Exception as e:
            print(f"⚠️ Failed to fetch attachment {att.name}: {e}")

    project_dir = tmp / req.task
    project_dir.mkdir()

    # --- Generate project ---
    try:
        print("🛠 Generating project from brief...")
        generate_project_from_brief(req.brief, req, project_dir, attachments_dir)
        print("✅ Project generation complete")
    except Exception as e:
        print(f"❌ LLM/template generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")

    # --- Pre-push secret scan and redaction ---
    def scan_and_redact(directory: Path):
        suspicious_markers = ["ghp_", "gho_", "AKIA", "AIza", "xoxb-"]
        sensitive_files = [".env", "secrets_map.json", "id_rsa", "id_ed25519"]
        for f in sensitive_files:
            p = directory / f
            if p.exists():
                try: p.unlink()
                except Exception: pass
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix.lower() not in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip"]:
                try:
                    text = path.read_text(encoding="utf-8")
                    for marker in suspicious_markers: text = text.replace(marker, "[REDACTED-]")
                    path.write_text(text, encoding="utf-8")
                except Exception: continue

    scan_and_redact(project_dir)
    print("🔒 Secret scan complete")

    # --- Determine repo ---
    email_user = req.email.split("@")[0]
    base = f"{slugify(req.task)}-{slugify(email_user)}"
    stable = hashlib.sha1(f"{req.email}-{req.task}".encode()).hexdigest()[:6]
    repo_name = f"{base}-{stable}"
    owner_or_org = GITHUB_OWNER.strip() if GITHUB_OWNER else ""

    try:
        org_account = await is_org_account(owner_or_org)
        print(f"[github] Using {'org' if org_account else 'personal'} account: {owner_or_org or 'personal'}")

        # --- Create or update repo ---
        repo_url, commit_sha, pages_url = create_or_upsert_github_repo_and_push(
            project_dir, repo_name, GITHUB_TOKEN,
            owner_or_org=(owner_or_org if org_account else None)
        )
        enable_github_pages(repo_url, GITHUB_TOKEN)
        print(f"📦 GitHub push complete: {repo_url}")

        # --- Wait for Pages ---
        async def wait_for_pages(url: str, attempts: int = 10):
            for i in range(attempts):
                try:
                    async with httpx.AsyncClient(timeout=20) as client:
                        r = await client.get(url, headers={"Cache-Control": "no-cache"})
                        if r.status_code == 200: return True
                except Exception: pass
                await asyncio.sleep(2 ** min(i, 4))
            return False

        await wait_for_pages(pages_url)
        print(f"🌐 GitHub Pages ready: {pages_url}")

    except Exception as e:
        print("❌ GitHub push error:", e)
        raise HTTPException(status_code=500, detail=f"GitHub error: {e}")

    # --- Notify evaluation system ---
    notify_payload = {
        "email": req.email,
        "task": req.task,
        "round": req.round,
        "nonce": req.nonce,
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url,
    }

    success = await post_with_retries(req.evaluation_url, notify_payload)
    response = {
        "status": "accepted",
        "task": req.task,
        "round": req.round,
        "notify_status": "notified" if success else "failed",
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url,
    }

    if not KEEP_BUILD_ARTIFACTS:
        shutil.rmtree(tmp, ignore_errors=True)
        print("🗑 Temp build artifacts cleaned")

    return response

# --- Mock evaluation endpoint ---
@app.post("/eval-mock")
async def eval_mock(payload: dict = Body(...)):
    print("[mock-eval] Received callback:", payload)
    return {"status": "ok"}
