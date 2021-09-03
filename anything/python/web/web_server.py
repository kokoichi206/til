import http.server
from socket import socket
import socketserver


# TCPServer とか、中身見てみても面白い
with socketserver.TCPServer(('127.0.0.1', 8000),
                http.server.SimpleHTTPRequestHandler) as httpd:
    httpd.serve_forever()
