import json
import time
import threading
import subprocess

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from http import HTTPStatus
from typing import TypeVar
from urllib.parse import urlparse

PORT = 8000

def __main__():
    thread = threading.Thread(target=httpServe)
    thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        return

def httpServe():
    handler = StubHttpRequestHandler
    httpd = HTTPServer(('',PORT),handler)
    httpd.serve_forever()

class StubHttpRequestHandler(BaseHTTPRequestHandler):
    server_version = "HTTP Stub/0.1"
    thread = None
    aviFilename = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_POST(self):
        content_len = int(self.headers.get('content-length'))
        requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))
        command = requestBody['contents']['command']
        args = ['irsend', 'SEND_ONCE', 'tv', command]
        res = ""
        try:
            res = subprocess.run(args, stdout=subprocess.PIPE)
        except:
            ""

        response = { 'status' : 200 }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        responseBody = json.dumps(response)

        self.wfile.write(responseBody.encode('utf-8'))

__main__()
