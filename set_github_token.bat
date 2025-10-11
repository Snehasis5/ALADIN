@echo off
echo Setting up GitHub Token for Automated Deployment
echo ================================================
echo.
echo To get a GitHub Personal Access Token:
echo 1. Go to https://github.com/settings/tokens
echo 2. Click "Generate new token" - "Generate new token (classic)"
echo 3. Give it a name like "Automated Deployment"
echo 4. Select these scopes:
echo    - repo (Full control of private repositories)
echo    - public_repo (Access public repositories)
echo    - admin:org (Full control of orgs and teams)
echo 5. Click "Generate token"
echo 6. Copy the token (it starts with "ghp_" or "gho_")
echo.
set /p GITHUB_TOKEN="Enter your GitHub token: "
if "%GITHUB_TOKEN%"=="" (
    echo No token entered. Exiting.
    pause
    exit /b 1
)
echo.
echo Setting GITHUB_TOKEN environment variable...
setx GITHUB_TOKEN "%GITHUB_TOKEN%"
echo.
echo [OK] GITHUB_TOKEN has been set for future sessions.
echo [OK] You can now run: python student_server.py
echo.
echo Note: You may need to restart your command prompt for the environment variable to take effect.
echo.
pause
