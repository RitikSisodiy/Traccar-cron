from flask import Flask
import requests
import os

# Configuration
URL = "https://traccer.onrender.com"  # Complete URL with protocol
HEALTHCHECK_ENDPOINT = "/login"  # Health check endpoint
TIMEOUT = 60  # Timeout for the request in seconds

# Retrieve environment variables
RENDER_API_TOKEN = os.getenv("RENDER_API_TOKEN")
SERVICE_ID = os.getenv("SERVICE_ID")

if not RENDER_API_TOKEN or not SERVICE_ID:
    print("Error: Environment variables RENDER_API_TOKEN and SERVICE_ID must be set.")
    exit(1)

def ping_website():
    try:
        # Send a HEAD request to the health check endpoint
        response = requests.head(f"{URL}{HEALTHCHECK_ENDPOINT}", timeout=TIMEOUT)

        # Consider both 200 and 302 as "up" statuses
        if response.status_code in [200, 302]:
            print("Website is up.")
            return True
        else:
            print(f"Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error accessing website: {e}")
        return False


def restart_service():
    try:
        # Headers for the POST request
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {RENDER_API_TOKEN}",
            "content-type": "application/json"
        }

        # Endpoint URL for the deploy request
        endpoint = f"https://api.render.com/v1/services/{SERVICE_ID}/deploys"

        # Send the POST request
        response = requests.post(endpoint, headers=headers)

        if response.status_code == 201:
            print("Service restart triggered successfully.")
            print("Response:", response.json())
        else:
            print("Failed to trigger service restart.")
            print("Status:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("Error occurred during service restart:", e)

def check_service():
    if not ping_website():
        print("Website is down. Restarting service...")
        restart_service()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def handle_request():
    check_service()
    return "Function triggered!", 200

@app.route("/health", methods=["GET"])
def health_request():
    return "working", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Default port to 5000 if not set
    app.run(port=port)
    
