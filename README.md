# ALADIN

![ALADIN Logo](./logo.png)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/Snehasis5/ALADIN)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## Project Description

**ALADIN** (Automated LLM Deployment and Integration Network) is a system that automates the generation of code via LLMs and deploys it automatically to GitHub.

It allows students or developers to submit tasks, attachments, and instructions to a FastAPI server, which:

- Generates a project based on the brief
- Saves attachments
- Commits and pushes the project to GitHub
- Enables GitHub Pages if applicable
- Notifies an evaluation endpoint with repository details

---

## Features

- Automated project generation from LLM instructions  
- Supports attachments like CSV, images, etc.  
- Automatic Git commit and push  
- GitHub Pages integration  
- Secret scanning to prevent sensitive data leaks

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Snehasis5/ALADIN.git
cd ALADIN
```

2. **Create a virtual environment:**

```bash
python -m venv venv
```

- **Linux/Mac:**

```bash
source venv/bin/activate
```

- **Windows (PowerShell):**

```powershell
venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**

- **Linux/Mac:**

```bash
export GITHUB_TOKEN="your_github_token"
export GITHUB_OWNER="your_github_username_or_org"
export API_SECRET_MAP="./secrets_map.json"
```

- **Windows PowerShell:**

```powershell
$env:GITHUB_TOKEN="your_github_token"
$env:GITHUB_OWNER="your_github_username_or_org"
$env:API_SECRET_MAP="./secrets_map.json"
```

---

## Usage

1. **Start the FastAPI server:**

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

2. **Send a POST request** to `/api-endpoint` with a task brief, attachments, and secret. Example using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api-endpoint \
-H "Content-Type: application/json" \
-d '{
  "email": "student@example.com",
  "secret": "your_secret_key",
  "task": "sum-of-sales",
  "round": 1,
  "nonce": "random_nonce",
  "brief": "Generate a single-page site that sums sales from a CSV.",
  "evaluation_url": "http://example.com/eval",
  "attachments": [
    {
      "name": "data.csv",
      "url": "data:text/csv;base64,..."
    }
  ]
}'
```

---

## What Happens Next

- The server generates the project based on your brief  
- Saves any attachments provided  
- Commits and pushes the project to GitHub automatically  
- Enables GitHub Pages (if applicable)  
- Notifies the evaluation URL with repository details

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
