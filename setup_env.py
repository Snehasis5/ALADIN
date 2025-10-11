#!/usr/bin/env python3
"""
Setup script to help configure the GitHub token for the automated deployment system.
"""

import os
import sys

def setup_github_token():
    print("GitHub Token Setup")
    print("=" * 50)
    print()
    print("To use this automated deployment system, you need a GitHub Personal Access Token.")
    print("This token will be used to create repositories and enable GitHub Pages.")
    print()
    print("Steps to get your GitHub token:")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Click 'Generate new token' -> 'Generate new token (classic)'")
    print("3. Give it a name like 'Automated Deployment'")
    print("4. Select these scopes:")
    print("   - repo (Full control of private repositories)")
    print("   - public_repo (Access public repositories)")
    print("   - admin:org (Full control of orgs and teams)")
    print("5. Click 'Generate token'")
    print("6. Copy the token (it starts with 'ghp_' or 'gho_')")
    print()
    
    # Check if token is already set
    current_token = os.getenv("GITHUB_TOKEN")
    if current_token:
        print(f"[OK] GITHUB_TOKEN is already set: {current_token[:8]}...")
        return True
    
    print("Current GITHUB_TOKEN status: [NOT SET]")
    print()
    
    # Try to set the token
    token = input("Enter your GitHub token (or press Enter to skip): ").strip()
    
    if not token:
        print("Skipping token setup. You can set it later by:")
        print("1. Setting environment variable: GITHUB_TOKEN=your_token_here")
        print("2. Creating a .env file with: GITHUB_TOKEN=your_token_here")
        return False
    
    # Set the token for this session
    os.environ["GITHUB_TOKEN"] = token
    print(f"[OK] GITHUB_TOKEN set for this session: {token[:8]}...")
    
    # Try to create .env file
    try:
        with open(".env", "w") as f:
            f.write(f"GITHUB_TOKEN={token}\n")
        print("[OK] Created .env file with your token")
    except Exception as e:
        print(f"[WARNING] Could not create .env file: {e}")
        print("You can create it manually with: GITHUB_TOKEN=your_token_here")
    
    return True

def test_configuration():
    print("\nTesting Configuration")
    print("=" * 30)
    
    try:
        from config import GITHUB_TOKEN
        if GITHUB_TOKEN:
            print("[OK] Configuration loaded successfully")
            print(f"[OK] GITHUB_TOKEN: {GITHUB_TOKEN[:8]}...")
            return True
        else:
            print("[ERROR] GITHUB_TOKEN not found in configuration")
            return False
    except Exception as e:
        print(f"[ERROR] Error loading configuration: {e}")
        return False

if __name__ == "__main__":
    print("Automated Deployment - Environment Setup")
    print("=" * 50)
    print()
    
    # Setup token
    token_set = setup_github_token()
    
    # Test configuration
    config_ok = test_configuration()
    
    print()
    if token_set and config_ok:
        print("[SUCCESS] Setup complete! You can now run the application.")
        print("To start the server: python student_server.py")
    else:
        print("[WARNING] Setup incomplete. Please set GITHUB_TOKEN and try again.")
        sys.exit(1)
