# config.py
"""
Configuration module for the automated deployment system.
Loads configuration from a .env file (if present) and environment variables.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ----------------------------------
# 1. Load .env explicitly
# ----------------------------------
# Find .env in the project root (same directory as this file)
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# ----------------------------------
# 2. Read values
# ----------------------------------
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER", "")
API_SECRET_MAP = os.getenv("API_SECRET_MAP", "secrets_map.json")
KEEP_BUILD_ARTIFACTS = os.getenv("KEEP_BUILD_ARTIFACTS", "false").lower() in ("true", "1", "yes")

# Optional LLM configuration
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com")  # OpenAI-compatible default
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# ----------------------------------
# 3. Diagnostics
# ----------------------------------
print(f"[config] Loaded .env from: {env_path}")
print(f"[config] GITHUB_OWNER={GITHUB_OWNER}")
print(f"[config] GITHUB_TOKEN found? {'✅' if GITHUB_TOKEN else '❌'}")

if not GITHUB_TOKEN:
    print("[WARNING] GITHUB_TOKEN not set. GitHub operations will fail.")
