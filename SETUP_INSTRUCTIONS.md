# Automated Deployment Setup Instructions

## Issue Fixed ✅

The import error in `student_server.py` has been resolved. The issue was:

1. **Missing `config.py` module** - Created a configuration module that loads settings from environment variables
2. **Missing PyGithub dependency** - Installed the required GitHub API library

## Current Status

- ✅ Server starts successfully
- ✅ All imports work correctly  
- ✅ Mock evaluation endpoint works (`/eval-mock`)
- ✅ Main API endpoint responds (requires GITHUB_TOKEN to be set)

## Next Steps - Setting up GitHub Token

To make the server fully functional, you need to set up a GitHub token:

### Option 1: Using the provided scripts
```bash
# Windows Batch
set_github_token.bat

# Windows PowerShell  
set_github_token.ps1

# Python setup
python setup_env.py
```

### Option 2: Manual setup
1. Create a GitHub Personal Access Token:
   - Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with permissions: `repo`, `pages`, `public_repo`
   - Copy the token

2. Set environment variable:
   ```bash
   setx GITHUB_TOKEN "your_token_here"
   ```

3. Or create a `.env` file:
   ```
   GITHUB_TOKEN=your_token_here
   GITHUB_OWNER=your_username  # optional
   ```

## Running the Server

```bash
# Start the server
python -m uvicorn student_server:app --reload --host 0.0.0.0 --port 8000

# Test the server
python test_server.py
```

## API Endpoints

- `GET /docs` - Interactive API documentation
- `POST /api-endpoint` - Main task processing endpoint
- `POST /eval-mock` - Mock evaluation callback endpoint

## Configuration

The server uses these environment variables:
- `GITHUB_TOKEN` (required) - GitHub personal access token
- `GITHUB_OWNER` (optional) - GitHub username/org for repos
- `API_SECRET_MAP` (optional) - Path to secrets JSON file (default: secrets_map.json)
- `KEEP_BUILD_ARTIFACTS` (optional) - Keep temp files for debugging (default: false)
