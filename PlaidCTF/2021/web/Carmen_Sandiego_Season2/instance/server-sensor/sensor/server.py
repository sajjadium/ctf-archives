from socketserver import ThreadingTCPServer, UnixStreamServer, BaseRequestHandler, StreamRequestHandler, ThreadingMixIn
import re
from threading import Lock, Thread
import time
import os
from queue import Queue

SENSOR_REGEX = r"([a-z]{1,512}): ([0-9a-zA-Z.+=-]+)"

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

					used_keys = { "ts" }
					data = []
					ok = True

					while True:
						line = self.rfile.readline().strip().decode("ascii")

						if line == "":
							break

						match = re.fullmatch(SENSOR_REGEX, line)

						if match is None:
							ok = False
							break
						else:
							key = match.group(1)
							value = match.group(2)

							if key in used_keys:
								ok = False
								break

							used_keys.add(key)
							data.append((key, value))

					if not ok:
						self.wfile.write(b"bad sensor data\n")
						continue

					now = "{:.3f}".format(time.time())

					with open("/var/www/goahead/data/data.txt", "a") as f:
						for key, value in data:
							with open(f"/var/www/goahead/data/latest/{key}", "w") as l:
								l.write(f"ts: {now}\n")
								l.write(f"value: {value}\n")
							f.write(f"{key}: {value}\n")
						f.write(f"ts: {now}\n")

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
