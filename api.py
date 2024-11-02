from http.server import BaseHTTPRequestHandler, HTTPServer
from main import check_service‎
import os
from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def handle_request():
    trigger_function()
    return "Function triggered!", 200

if __name__ == "__main__":
    app.run(int(port=os.getenv("PORT"))

