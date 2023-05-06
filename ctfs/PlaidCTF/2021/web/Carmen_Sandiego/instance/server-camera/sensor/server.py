from socketserver import ThreadingTCPServer, UnixStreamServer, BaseRequestHandler, StreamRequestHandler, ThreadingMixIn
import re
from threading import Lock, Thread
import time
import os
from queue import Queue

KEY_REGEX = r"([a-z]{1,512})"

connection_lock = Lock()

class ThreadingUnixStreamServer(ThreadingMixIn, UnixStreamServer):
	pass

def start_tcp(queue):
	class TcpHandler(StreamRequestHandler):
		def handle(self):
			self.wfile.write(b"token\n")
			token = self.rfile.readline().strip()

			if token != os.environ["SENSOR_TOKEN"].encode("ascii"):
				self.wfile.write(b"bad token\n")
				return

			if not connection_lock.acquire(blocking = False):
				self.wfile.write(b"already have a connection\n")
				return

			self.wfile.write(b"ok\n")

			try:
				while True:
					while True:
						try:
							cmd = queue.get_nowait()
							self.wfile.write(cmd + b"\n")
						except:
							break

					name = self.rfile.readline().strip().decode("ascii")

					if not re.fullmatch(KEY_REGEX, name):
						self.wfile.write(b"bad camera name\n")
						continue

					try:
						length = int(self.rfile.readline().strip())
						if length > 1024 * 1024:
							raise Exception()
					except:
						self.wfile.write(b"bad length\n")
						continue

					image = self.rfile.read(length)

					with open(f"/var/www/goahead/data/snapshot/{name}", "wb") as f:
						f.write(image)

					self.wfile.write(b"ok\n")
			finally:
				connection_lock.release()

	tcp = ThreadingTCPServer(("0.0.0.0", 9999), TcpHandler)
	tcp.serve_forever()

def start_unix(queue):
	class UnixHandler(StreamRequestHandler):
		def handle(self):
			while True:
				cmd = self.rfile.readline()

				if len(cmd) == 0:
					return

				cmd = cmd.strip()
				queue.put_nowait(cmd)

	unix = ThreadingUnixStreamServer("/sensor/sensor.sock", UnixHandler)
	unix.serve_forever()

if __name__ == "__main__":
	queue = Queue()

	Thread(target = start_tcp, args = (queue,)).start()
	Thread(target = start_unix, args = (queue,)).start()
