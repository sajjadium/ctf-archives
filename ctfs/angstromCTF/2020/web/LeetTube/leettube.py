#!/usr/bin/env python
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

videos = []
for file in os.listdir('videos'):
	os.chmod('videos/'+file, 0o600)
	videos.append({'title': file.split('.')[0], 'path': 'videos/'+file, 'content': open('videos/'+file, 'rb').read()})
published = []
for video in videos:
	if video['title'].startswith('UNPUBLISHED'): os.chmod(video['path'], 0) # make sure you can't just guess the filename
	else: published.append(video)

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			self.path = urllib.parse.unquote(self.path)
			if self.path.startswith('/videos/'):
				file = os.path.abspath('.'+self.path)
				try: video = open(file, 'rb', 0)
				except OSError:
					self.send_response(404)
					self.end_headers()
					return
				reqrange = self.headers.get('Range', 'bytes 0-')
				ranges = list(int(i) for i in reqrange[6:].split('-') if i)
				if len(ranges) == 1: ranges.append(ranges[0]+65536)
				try:
					video.seek(ranges[0])
					content = video.read(ranges[1]-ranges[0]+1)
				except:
					self.send_response(404)
					self.end_headers()
					return
				self.send_response(206)
				self.send_header('Accept-Ranges', 'bytes')
				self.send_header('Content-Type', 'video/mp4')
				self.send_header('Content-Range', 'bytes '+str(ranges[0])+'-'+str(ranges[0]+len(content)-1)+'/'+str(os.path.getsize(file)))
				self.end_headers()
				self.wfile.write(content)
			elif self.path == '/':
				self.send_response(200)
				self.send_header('Content-Type', 'text/html')
				self.end_headers()
				self.wfile.write(("""
<style>
body {
	background-color: black;
	color: #00e33d;
	font-family: monospace;
	max-width: 30em;
	font-size: 1.5em;
	margin: 2em auto;
}
</style>
<h1>LeetTube</h1>
<p>There are <strong>"""+str(len(published))+"</strong> published video"+('s' if len(published) > 1 else '')+" and <strong>"+str(len(videos)-len(published))+"</strong> unpublished video"+('s' if len(videos)-len(published) > 1 else '')+".</p>"+''.join("<h2>"+video["title"]+"</h2><video controls src=\""+video["path"]+"\"></video>" for video in published)).encode('utf-8'))
			else:
				self.send_response(404)
				self.end_headers()
		except:
			self.send_response(500)
			self.end_headers()

httpd = HTTPServer(('', 8000), RequestHandler)
httpd.serve_forever()
