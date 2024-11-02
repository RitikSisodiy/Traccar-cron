from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from flask import Flask


import http.client
import json
import os

# Configuration
URL = "traccer.onrender.com"  # Host without protocol
HEALTHCHECK_ENDPOINT = "/healthcheck"  # Health check endpoint
TIMEOUT = 60  # Timeout for the request in seconds

# Retrieve environment variables
RENDER_API_TOKEN = os.getenv("RENDER_API_TOKEN")
SERVICE_ID = os.getenv("SERVICE_ID")

if not RENDER_API_TOKEN or not SERVICE_ID:
    print("Error: Environment variables RENDER_API_TOKEN and SERVICE_ID must be set.")
    exit(1)

def ping_website():
    try:
        # Establish a connection
        connection = http.client.HTTPSConnection(URL, timeout=TIMEOUT)
        connection.request("GET", HEALTHCHECK_ENDPOINT)
        response = connection.getresponse()

        if response.status == 200:
            print("Website is up.")
            return True
        else:
            print(f"Unexpected status code: {response.status}")
            return False
    except Exception as e:
        print(f"Error accessing website: {e}")
        return False
    finally:
        # Ensure the connection is closed
        connection.close()

def restart_service():
    try:
        # Establish HTTPS connection to the Render API
        connection = http.client.HTTPSConnection("api.render.com")

        # Headers for the POST request
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {RENDER_API_TOKEN}",
            "content-type": "application/json"
        }

        # Endpoint URL for the deploy request
        endpoint = f"/v1/services/{SERVICE_ID}/deploys"

        # Send the POST request
        connection.request("POST", endpoint, headers=headers)

        # Get the response
        response = connection.getresponse()
        data = response.read().decode()

        if response.status == 201:
            print("Service restart triggered successfully.")
            print("Response:", data)
        else:
            print("Failed to trigger service restart.")
            print("Status:", response.status)
            print("Response:", data)

    except Exception as e:
        print("Error occurred during service restart:", e)
    finally:
        # Ensure the connection is closed
        connection.close()

def check_service():
    if not ping_website():
        print("Website is down. Restarting service...")
        restart_service()


app = Flask(__name__)

@app.route("/", methods=["GET"])
def handle_request():
    trigger_function()
    return "Function triggered!", 200

if __name__ == "__main__":
    app.run(int(port=os.getenv("PORT")))

