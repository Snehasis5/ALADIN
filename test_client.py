import requests
import base64
import json

# -----------------------------
# Config
# -----------------------------
STUDENT_API = "http://127.0.0.1:8000/api-endpoint"
EVALUATION_URL = "http://127.0.0.1:8000/eval-mock"

# -----------------------------
# Optional attachment: example markdown input (can remove if not needed)
# -----------------------------
markdown_text = "# Sample Input\nThis is an example input file."
encoded_md = base64.b64encode(markdown_text.encode("utf-8")).decode("utf-8")

# -----------------------------
# Task payload: LLM-generated web app
# -----------------------------
payload = {
    "email": "student@example.com",
    "secret": "my-shared-secret",
    "task": "llm-generated-web-app",
    "round": 1,
    "nonce": "abcd-1234",
    "brief": """
Create a fully functional web application using modern web technologies (HTML, CSS, JavaScript):

1. The app should be directly viewable in a browser, hosted via GitHub Pages.
2. Include an index.html as the main entry point.
3. All dependencies must be included via CDN links or simple scripts (no private or local dependencies).
4. Provide an interactive UI demonstrating the app’s functionality (e.g., a simple calculator, a Markdown previewer, or a to-do list).
5. Include a README.md explaining what the app does and how to use it.
6. Ensure the app is self-contained, safe, and ready-to-run immediately after GitHub Pages deployment.
7. Attach any example input files if needed to make the app functional out-of-the-box.
""",
    "checks": [
        "README.md exists",
        "index.html loads all required scripts",
        "App UI is interactive"
    ],
    "evaluation_url": EVALUATION_URL,
    "attachments": [
        {
            "name": "example_input.md",
            "url": f"data:text/markdown;base64,{encoded_md}"
        }
    ]
}

# -----------------------------
# Send POST request
# -----------------------------
try:
    print("Sending Round 1 task to student API...")
    response = requests.post(STUDENT_API, json=payload, timeout=120)
    
    # Raise exception for HTTP errors
    response.raise_for_status()
    
    response_json = response.json()
    
    print("\nResponse status:", response.status_code)
    print("Response body:\n", json.dumps(response_json, indent=2))
    
    # Print GitHub Pages URL if available
    pages_url = response_json.get("pages_url")
    if pages_url:
        print("\n🔗 Your LLM-generated app is live at:", pages_url)
    else:
        print("\n⚠️ Pages URL not returned. Check server logs.")
except requests.exceptions.HTTPError as http_err:
    print(f"❌ HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as req_err:
    print(f"❌ Request error occurred: {req_err}")
except json.JSONDecodeError as json_err:
    print(f"❌ Failed to parse JSON response: {json_err}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
