#!/usr/bin/python3

import os
import socketserver
import urllib.request
from os.path import abspath
from http.server import SimpleHTTPRequestHandler
from urllib.parse import unquote, urlparse, urljoin

PORT = 9097

whitelist = ["http://127.0.0.1/static/images/", "http://localhost/static/images/"]
blacklist = ["admin","flag"]
remove_list = ["'","OR","SELECT","FROM",";","../","./","....//"]

def waf(url):
	resp = unquote(url)
	whitelist_check = False
	for uri in whitelist:
		if resp.lower().startswith(uri):
			whitelist_check = uri
			break
	if whitelist_check == False:
		return None
	for forbidden in blacklist:
		if forbidden in resp.lower():
			return None
	for badstr in remove_list:
		resp = resp.replace(badstr,"BLOCKEDBY1337WAF")
	resp = urlparse(resp)
	resp = unquote(abspath(resp.path))
	return urljoin(whitelist_check,resp)

class CDNProxy(SimpleHTTPRequestHandler):
	def do_GET(self):
		url = self.path[1:]
		print(self.headers)
		self.send_response(200)
		self.send_header("X-CDN","CDN-1337")
		self.end_headers()
		waf_result = waf(url)
		if waf_result:
			self.copyfile(urllib.request.urlopen(waf_result), self.wfile)
		else:
			self.wfile.write(bytes("1337 WAF blocked your request","utf-8"))

httpd = socketserver.ForkingTCPServer(('', PORT), CDNProxy)
print("Now serving at " + str(PORT))
httpd.serve_forever()