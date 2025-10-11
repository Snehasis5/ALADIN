# evaluate.py
"""
Evaluate repos stored in repos.db (inserted by evaluation_receiver.py)
Per repo: clone repo, check license, README quality (placeholder), run JS checks by loading pages_url using Playwright.
"""

import sqlite3
import os
import tempfile
import subprocess
import requests
from pathlib import Path
from playwright.sync_api import sync_playwright

DB_PATH = os.getenv("REPOS_DB", "repos.db")
CLONE_DIR = Path(tempfile.gettempdir()) / "repo-clones"

def get_pending_repos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, email, task, round, repo_url, commit_sha, pages_url FROM repos")
    rows = c.fetchall()
    conn.close()
    return rows

def check_mit_license(local_dir: Path):
    # check if LICENSE exists and contains MIT
    f = local_dir / "LICENSE"
    if not f.exists():
        return False, "LICENSE missing"
    txt = f.read_text().lower()
    return ("mit license" in txt) or ("permission is hereby granted" in txt), "ok" if "mit license" in txt else "nonstandard"

def run_playwright_checks(pages_url, checks):
    # Checks are JS snippets that should evaluate truthy in the page
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(pages_url, wait_until="load", timeout=15000)
        # Evaluate each js check in the page context
        for js in checks:
            snippet = js
            try:
                ok = page.evaluate(snippet)
            except Exception as e:
                ok = False
            results.append((js, bool(ok)))
        browser.close()
    return results

def clone_repo(repo_url):
    tmp = CLONE_DIR / repo_url.split("/")[-1]
    tmp.mkdir(parents=True, exist_ok=True)
    if (tmp / ".git").exists():
        # do pull
        subprocess.check_call(["git", "pull"], cwd=str(tmp))
    else:
        subprocess.check_call(["git", "clone", repo_url, str(tmp)])
    return tmp

def main():
    rows = get_pending_repos()
    for r in rows:
        id_, email, task, round_, repo_url, commit_sha, pages_url = r
        print("Evaluating", repo_url)
        try:
            local = clone_repo(repo_url)
        except Exception as e:
            print("clone failed", e)
            continue
        lic_ok, lic_reason = check_mit_license(local)
        print("LICENSE:", lic_ok, lic_reason)
        # README quality: place holder — send README text to LLM for scoring in your full system
        readme = (local / "README.md").read_text() if (local / "README.md").exists() else ""
        # Playwright checks: in this demo we attempt a sanity load and simple checks if present
        try:
            # Example check set: you would derive from task template stored earlier; for now try sample checks
            checks = [
                "!!document.querySelector('#total-sales')",
                "!!document.querySelector('#markdown-output')",
                "!!document.querySelector('#github-created-at')",
            ]
            results = run_playwright_checks(pages_url, checks)
            print("Playwright results:", results)
        except Exception as e:
            print("playwright failed", e)

if __name__ == "__main__":
    main()
