# PowerShell script to set up GitHub Token
Write-Host "Setting up GitHub Token for Automated Deployment" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "To get a GitHub Personal Access Token:" -ForegroundColor Yellow
Write-Host "1. Go to https://github.com/settings/tokens" -ForegroundColor White
Write-Host "2. Click 'Generate new token' - 'Generate new token (classic)'" -ForegroundColor White
Write-Host "3. Give it a name like 'Automated Deployment'" -ForegroundColor White
Write-Host "4. Select these scopes:" -ForegroundColor White
Write-Host "   - repo (Full control of private repositories)" -ForegroundColor White
Write-Host "   - public_repo (Access public repositories)" -ForegroundColor White
Write-Host "   - admin:org (Full control of orgs and teams)" -ForegroundColor White
Write-Host "5. Click 'Generate token'" -ForegroundColor White
Write-Host "6. Copy the token (it starts with 'ghp_' or 'gho_')" -ForegroundColor White
Write-Host ""

$token = Read-Host "Enter your GitHub token"
if ([string]::IsNullOrEmpty($token)) {
    Write-Host "No token entered. Exiting." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Setting GITHUB_TOKEN environment variable..." -ForegroundColor Yellow
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $token, "User")

Write-Host ""
Write-Host "[OK] GITHUB_TOKEN has been set for future sessions." -ForegroundColor Green
Write-Host "[OK] You can now run: python student_server.py" -ForegroundColor Green
Write-Host ""
Write-Host "Note: You may need to restart your command prompt for the environment variable to take effect." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue"
