import os
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', "text/html")
    self.end_headers()
    self.wfile.write(b'<html>It works!</html>')

  def do_POST(self):
    flag = os.environ.get('FLAG')
    if not flag:
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'Something went wrong. Please call admin.')
      return

    if self.path != '/showmeflag':
      self.send_response(200)
      self.send_header('Content-Type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'Idiot')
      return

    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.end_headers()
    self.wfile.write(flag.encode())

server_address = ('0.0.0.0', 3000)
httpd = HTTPServer(server_address, MyHTTPRequestHandler)
httpd.serve_forever()
