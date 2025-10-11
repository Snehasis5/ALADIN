# round1.py
"""
Read submissions.csv and POST generated tasks to student endpoints.
Each row in submissions.csv: timestamp,email,endpoint,secret
This script will generate a task.json and POST it to the endpoint.
"""

import csv
import httpx
import uuid
import hashlib
from datetime import datetime
import random, base64, json

SUBMISSIONS_CSV = "submissions.csv"  # timestamp,email,endpoint,secret
TEMPLATES = [
    {
        "id": "sum-of-sales",
        "brief": "Publish a single-page site that fetches data.csv from attachments, sums its sales column, sets the title to 'Sales Summary {seed}', displays the total inside #total-sales, and loads Bootstrap 5 from jsdelivr.",
        "attachments": [{"name":"data.csv","url": None}],  # will fill seed-based CSV
        "checks": ["js: document.title.includes('Sales Summary')", "js: !!document.querySelector('#total-sales')"]
    },
    {
        "id": "markdown-to-html",
        "brief": "Publish a static page that converts input.md from attachments to HTML with marked, renders it inside #markdown-output, and loads highlight.js for code blocks.",
        "attachments": [{"name":"input.md","url": None}],
        "checks": ["js: !!document.querySelector('#markdown-output')"]
    },
    {
        "id": "github-user-created",
        "brief": "Publish a Bootstrap page with form id='github-user-{seed}' that fetches a GitHub username and shows creation date in #github-created-at.",
        "attachments": [],
        "checks": ["js: document.querySelector('#github-created-at')"]
    },
    {
        "id": "captcha-solver",
        "brief": "Create a captcha solver that handles ?url=https://.../image.png. Default to attached sample.",
        "attachments": [{"name":"sample.png","url": None}],
        "checks": ["js: !!document.querySelector('#img')","js: !!document.querySelector('#result')"]
    },
]

def make_seed(email):
    s = email + datetime.utcnow().strftime("%Y-%m-%d-%H")
    return hashlib.sha1(s.encode()).hexdigest()[:12]

def create_attachment_data(template, seed):
    # For data.csv create a small csv base64 encoded
    for att in template.get("attachments", []):
        if att["name"] == "data.csv":
            rows = "product,region,sales\nA,IN,100\nB,IN,200\nC,US,300\n"
            att["url"] = "data:text/csv;base64," + base64.b64encode(rows.encode()).decode()
        elif att["name"] == "input.md":
            md = f"# Sample markdown {seed}\n\n- hello\n\n```python\nprint('hi')\n```\n"
            att["url"] = "data:text/markdown;base64," + base64.b64encode(md.encode()).decode()
        elif att["name"] == "sample.png":
            # small transparent 1x1 PNG base64
            tiny_png = ("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4"
                        "////fwAJ/wP+WfJ/AAAAAElFTkSuQmCC")
            att["url"] = "data:image/png;base64," + tiny_png

def pick_template(seed):
    return random.choice(TEMPLATES)

async def post_task(endpoint, payload):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(endpoint, json=payload)
        return r.status_code, r.text

import asyncio

async def main():
    rows = []
    with open(SUBMISSIONS_CSV) as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    for r in rows:
        email = r["email"]
        endpoint = r["endpoint"]
        secret = r["secret"]
        seed = make_seed(email)
        template = pick_template(seed)
        create_attachment_data(template, seed)
        task_id = f"{template['id']}-{seed[:6]}"
        payload = {
            "email": email,
            "secret": secret,
            "task": task_id,
            "round": 1,
            "nonce": str(uuid.uuid4()),
            "brief": template["brief"].replace("{seed}", seed),
            "checks": template["checks"],
            "evaluation_url": os.getenv("EVALUATION_URL", "http://localhost:8001/repo-callback"),
            "attachments": template.get("attachments", [])
        }
        print(f"Posting task {task_id} -> {endpoint}")
        status, text = await post_task(endpoint, payload)
        print("status", status, "text", text)

if __name__ == "__main__":
    asyncio.run(main())
