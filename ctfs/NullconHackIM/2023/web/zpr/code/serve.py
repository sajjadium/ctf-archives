from functools import partial
import http.server
import re

PORT = 8088
HOST = "0.0.0.0"

http.server.SimpleHTTPRequestHandler._orig_list_directory = http.server.SimpleHTTPRequestHandler.list_directory

def better_list_directory(self, path):
	if not re.match(r"^/tmp/data/[0-9a-f]{32}", path):
		return None
	else:
		return self._orig_list_directory(path)

http.server.SimpleHTTPRequestHandler.list_directory = better_list_directory


Handler = partial(http.server.SimpleHTTPRequestHandler, directory="/tmp/data/")
Server = http.server.ThreadingHTTPServer


with Server((HOST, PORT), Handler) as httpd:
    httpd.serve_forever()