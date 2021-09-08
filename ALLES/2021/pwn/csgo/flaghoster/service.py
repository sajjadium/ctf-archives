from http.server import BaseHTTPRequestHandler
import socketserver
import os

class Handler(BaseHTTPRequestHandler):
    def do_FLAG(self):
        cl = int(self.headers['Content-Length'])
        data = self.rfile.read(cl)
        if data == b"is for me?":
            self.send_response(418)
            self.send_header('Content-type', 'text/flag')
            self.end_headers()
            self.wfile.write(os.environ.get('FLAG').encode())
            return
        self.send_response(406)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()


with socketserver.TCPServer(("", 31337), Handler) as httpd:
    httpd.serve_forever()