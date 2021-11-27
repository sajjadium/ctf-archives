#!/usr/bin/env python3
import threading
import socket
import subprocess
import os
import time
import stat
import fcntl
import struct

STATIC_FILES = [
  ('/index.html', 'text/html;charset=utf-8'),
  ('/banner.png', 'image/png'),
  ('/favicon.ico', 'image/png'),
]

STATIC_FILE_CONTENT = {}

SERVER_BANNER = "AdvancedNetcatIGuess v0.1"

def meh(s, status, message):
  html = (
      '<h1>Well yes, but actually no.</h1>' +
      f'<p>{message}</p>'
  )

  s.sendall(bytes(
      f'HTTP/1.1 {str(status)} {message}\r\n' +
      f'Server: {SERVER_BANNER}\r\n' +
      'Content-Type: text/html;charset=utf-8\r\n' +
      f'Content-Length: {str(len(html))}\r\n' +
      '\r\n' + html,
      "utf-8")
  )
  block_until_buffer_empty(s)
  s.shutdown(socket.SHUT_RDWR)
  s.close()

def validate_param_name(param):
  ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789_")
  return all(p in ALLOWED_CHARS for p in param)

def recode_param_value(value):
  decoded = []

  i = 0
  while i < len(value):
    if value[i] == '%':
      if i + 2 >= len(value):
        return None
      try:
        decoded.append(int(value[i+1:i+3], 16))
      except ValueError:
        return None
      i += 3
    else:
      decoded.append(ord(value[i]))
      i += 1

  # Just URL-encode everything w/e.
  final = ''.join(["%%%.2x" % v for v in decoded])
  return final


def handle_cgi(s, addr, method, uri):
  # Check who's a teapot.
  uri = uri[len('/cgi-bin/'):]
  if '/' in uri or '..' in uri:
    return meh(s, 418, "I'm a teapot")

  query_part = ""
  uri_split = uri.split("?", 1)
  file_name = uri_split[0]

  if not file_name:
    return meh(s, 418, "I'm a teapot")

  file_path = f'./cgi-bin/{file_name}'
  if not os.path.isfile(file_path):
    return meh(s, 404, "You're a teapot")

  if file_name.lower() == "x":
    return meh(s, 403,
      "Well, running x would give you the flag, so how about no.")

  # Parse the query.
  if len(uri_split) > 1:
    query_part = uri_split[1]

  query = []
  if query_part:
    query = [ e.split("=", 1) for e in query_part.split("&") ]
    query = [ e for e in query if len(e) == 2 and e[0] ]

  for i in range(len(query)):
    if not validate_param_name(query[i][0]):
      return meh(s, 418, "I'm a teapot")

    res = recode_param_value(query[i][1])
    if res is None:
      return meh(s, 418, "I'm a teapot")
    query[i][1] = res

  st = os.stat(file_path)
  if not (st.st_mode & stat.S_IEXEC):
    try:
      os.chmod(file_path, st.st_mode | stat.S_IEXEC)
    except PermissionError:
      return meh(s, 503, "Service Unavailable")

  # Read headers (and ignore them).
  while True:
    data = []

    # Get header byte by byte.
    while True:
      d = s.recv(1)
      if not d:
        s.close()
        return

      data.append(d)
      if d == b'\n':
        break

    header_line = b''.join(data).strip()
    if not header_line:
      break  # End of headers.

  # Run the script in a better CGI environment.
  client_env = os.environ.copy()
  for k, v in query:
    env_name = f'QUERY_PARAM_{k.upper()}'
    client_env[env_name] = v

  client_dir = os.path.dirname(os.path.realpath(__file__)) + "/cgi-bin"

  full_path = os.path.realpath(file_path)
  print(f"Starting process {file_path}")
  try:
    subprocess.run(
      [ full_path ],
      stdin=s.fileno(),
      stdout=s.fileno(),
      timeout=2,
      cwd=client_dir,
      env=client_env)
  except Exception as e:
    print(e)

  print(f"Finished {file_path}")
  block_until_buffer_empty(s)
  s.shutdown(socket.SHUT_RDWR)
  s.close()

def handle_static(s, addr, method, uri):
  # Read headers? Meh.

  if method != "GET":
    return meh(s, 405, "Method Not Allowed")

  if uri == "/":
    uri = "/index.html"

  if uri not in STATIC_FILE_CONTENT:
    return meh(s, 418, "I'm a teapot")

  f = STATIC_FILE_CONTENT[uri]

  content_length = str(len(f["content"]))

  s.sendall(bytes(
      'HTTP/1.1 200 OK\r\n' +
      f'Server: {SERVER_BANNER}\r\n' +
      f'Content-Type: {f["mime_type"]}\r\n' +
      f'Content-Length: {len(f["content"])}\r\n' +
      '\r\n',
      "utf-8")
  )
  s.sendall(f["content"])
  block_until_buffer_empty(s)
  s.shutdown(socket.SHUT_RDWR)
  s.close()

def handle_connection(s, addr):
  print(f"Handling connection {addr}")

  try:
    data = []

    # Get header byte by byte.
    while True:
      d = s.recv(1)
      if not d:
        s.close()
        return

      data.append(d)
      if d == b'\n':
        break

    header_line = str(b''.join(data), 'utf-8')
    method, uri, version = header_line.split(' ')

    if not uri.startswith('/cgi-bin/'):
      return handle_static(s, addr, method, uri)

    return handle_cgi(s, addr, method, uri)

  except socket.error:
    s.close()
    return

  block_until_buffer_empty(s)
  s.shutdown(socket.SHUT_RDWR)
  s.close()

def block_until_buffer_empty(s):
  while left_to_ACK_byte_count(s):
    time.sleep(0.1)

def left_to_ACK_byte_count(s):
  SIOCOUTQ = 0x5411
  return struct.unpack("I", fcntl.ioctl(s.fileno(), SIOCOUTQ, '\0\0\0\0'))[0]

def main():
  for fname, mime_type in STATIC_FILES:
    with open(f'static/{fname}', 'rb') as f:
      content = f.read()

    STATIC_FILE_CONTENT[fname] = {
      "mime_type": mime_type,
      "content": content
    }

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 8888))
    s.listen(256)

    while True:
      conn, addr = s.accept()
      print(f"Connection from: {addr}")

      th = threading.Thread(
          target=handle_connection,
          args=(conn, addr),
          daemon=True
      )
      th.start()

if __name__ == "__main__":
  main()
