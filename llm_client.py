# llm_client.py
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Updated constants based on AI Pipe documentation
LLM_API_KEY = os.getenv("LLM_API_KEY")  # Changed from LLM_API_KEY to AIPIPE_TOKEN
LLM_ENDPOINT = "https://aipipe.org/openai/v1/chat/completions"  # Corrected endpoint

def is_configured() -> bool:
    """Check if AI Pipe is properly configured."""
    return bool(LLM_API_KEY)

def generate_site_files_via_llm(brief: str, attachments: list[dict]) -> dict | None:
    """
    Uses an LLM through AI Pipe to generate deployable static site code.
    Returns a dict with keys: index_html, main_js, readme
    """

    if not is_configured():
        print("⚠️ AIPIPE_TOKEN not configured. Set AIPIPE_TOKEN environment variable.")
        print("💡 Get your token from: https://aipipe.org/login")
        return None

    # Enhanced prompt for better JSON generation
    system_prompt = """You are a expert web developer that generates complete, deployable static websites.
You MUST return ONLY valid JSON with this exact structure:
{
  "index_html": "<!DOCTYPE html>\\n<html>\\n<head>...</head>\\n<body>...</body>\\n</html>",
  "main_js": "// JavaScript code here",
  "readme": "# Project\\n\\nDescription..."
}

Requirements for each file:
- index_html: Must be a complete, valid HTML5 document with proper structure
- main_js: JavaScript code that can be included in a script tag
- readme: Markdown file with setup instructions and license

Do NOT include any text, explanations, or markdown code fences outside the JSON.
"""

    user_prompt = f"""
BRIEF: {brief}

Generate a complete, self-contained static website that fulfills the brief.
Use only plain HTML, CSS, and vanilla JavaScript (no external dependencies unless necessary).
Make sure all code is properly formatted and ready to run.

Return ONLY the JSON object with the three required keys.
"""

    payload = {
        "model": "gpt-4o-mini",  # AI Pipe supports various models
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.1,  # Low temperature for consistent JSON
        "max_tokens": 4000,
    }

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        print("🔄 Calling AI Pipe API...")
        response = requests.post(LLM_ENDPOINT, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        print("✅ Received AI Pipe response")
        
        # Parse the JSON response
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
            # Try to extract JSON if it's wrapped
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = content[start:end]
                data = json.loads(json_str)
            else:
                print(f"🔍 Raw response preview: {content[:200]}...")
                raise ValueError("No valid JSON found in response")

        # Validate response structure
        required_keys = {"index_html", "main_js", "readme"}
        if not all(key in data for key in required_keys):
            missing = required_keys - set(data.keys())
            raise ValueError(f"Missing required keys: {missing}")

        return data

    except requests.exceptions.ConnectionError as e:
        print(f"⚠️ Connection error: {e}")
        print("💡 Check your internet connection and the AI Pipe service status")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ HTTP error {response.status_code}: {e}")
        if response.status_code == 401:
            print("🔑 Authentication failed. Check your AIPIPE_TOKEN")
            print("💡 Get your token from: https://aipipe.org/login")
        elif response.status_code == 429:
            print("⏳ Rate limit exceeded. Try again later.")
        return None
    except Exception as e:
        print(f"⚠️ AI Pipe generation failed: {e}")
        return None

def check_usage():
    """Check your AI Pipe usage statistics."""
    if not is_configured():
        print("⚠️ AIPIPE_TOKEN not configured")
        return None
    
    try:
        response = requests.get(
            "https://aipipe.org/usage",
            headers={"Authorization": f"Bearer {LLM_API_KEY}"},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"⚠️ Usage check failed: {e}")
        return None

def test_ai_pipe_connection():
    """Test the AI Pipe connection with a simple request."""
    if not is_configured():
        print("❌ AIPIPE_TOKEN not set")
        print("💡 Get your token from: https://aipipe.org/login")
        return False
    
    # Test with a simple prompt
    test_prompt = "Create a simple HTML page with a heading that says 'Hello World'"
    
    try:
        result = generate_site_files_via_llm(test_prompt, [])
        if result and "index_html" in result:
            print("✅ AI Pipe connection test passed!")
            print(f"📄 Generated HTML preview: {result['index_html'][:100]}...")
            return True
        else:
            print("❌ AI Pipe test failed - no valid response")
            return False
    except Exception as e:
        print(f"❌ AI Pipe connection test error: {e}")
        return False

if __name__ == "__main__":
    # Test the connection when run directly
    print("🧪 Testing AI Pipe configuration...")
    
    # Check usage first
    usage = check_usage()
    if usage:
        print(f"📊 Usage stats: {usage}")
    
    # Test connection
    test_ai_pipe_connection()