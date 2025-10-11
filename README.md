# ALADIN

![ALADIN Logo](./logo.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](#)

**Automated LLM Assistant for Deployment and Integration**  

ALADIN is a powerful tool that automates LLM-generated code and seamlessly deploys it to GitHub, enabling developers to focus on creativity while handling repetitive deployment tasks automatically.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Overview

ALADIN streamlines the workflow of developers who work with LLM-generated code. With ALADIN, you can:

- Generate project code from textual briefs using LLMs.  
- Automatically commit and push code to GitHub repositories.  
- Enable GitHub Pages for deployed projects.  
- Perform secret scanning and redaction to prevent leaks.  
- Handle attachments and project assets automatically.  

ALADIN is perfect for hackathons, rapid prototyping, or any automated coding workflow where deployment efficiency matters.

---

## Features

- **LLM Code Automation:** Automatically generate code from textual descriptions.  
- **Automated GitHub Deployment:** Create/update repositories and push changes automatically.  
- **Secret Scan & Redaction:** Ensures sensitive information is never committed.  
- **Attachment Handling:** Automatically downloads and organizes project assets.  
- **GitHub Pages Integration:** Enable live web hosting for projects.  
- **Cross-Platform Support:** Runs on local machines or Render cloud deployments.  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Snehasis5/ALADIN.git
cd ALADIN
git clone https://github.com/Snehasis5/ALADIN.git
cd ALADIN
```

2. Create a virtual environment:
```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
export GITHUB_TOKEN="your_github_token"
export GITHUB_OWNER="your_github_username_or_org"
export API_SECRET_MAP="./secrets_map.json"


// For Windows PowerShell, use $env:GITHUB_TOKEN="your_github_token" instead of export.
```
Usage

Start the FastAPI server:
```
uvicorn server:app --host 0.0.0.0 --port 8000
```

Send a POST request to /api-endpoint with a task brief, attachments, and secret. Example using curl:
```
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
What happens next

The server generates the project based on your brief.

Saves any attachments provided.

Commits and pushes the project to GitHub automatically.

Enables GitHub Pages (if applicable).

Notifies the evaluation URL with repository details.
venv\Scripts\activate
'''
