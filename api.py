from http.server import BaseHTTPRequestHandler, HTTPServer
from main import check_service‎
import os
def trigger_function():
    print("Function triggered!")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Trigger the function on any GET request
        check_service‎()
        
        # Send a basic response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Function triggered!')

# Server settings
port = int(os.getenv("PORT"))
server_address = ('', port)
httpd = HTTPServer(server_address, SimpleHandler)

print(f"Server running on port {port}")
httpd.serve_forever()
