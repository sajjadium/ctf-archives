import socketserver, string

def check_safe(line):
    return all(c in (string.ascii_letters + string.digits + string.whitespace + '+=#').encode() for c in line)

class AaaSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request

        try:
            buf, env = bytearray(), {}
            while data := conn.recv(1024):
                buf += data

                if b'\n' in buf:
                    line, buf = buf.split(b'\n', 2)
                    if check_safe(line):
                        exec(line, {}, env)
                        conn.send(str(env).encode() + b'\n')
                    else:
                        conn.send(b"This is just an adder, what are you trying to do :'(\n")
                        conn.close()
                        break
        except Exception as e:
            print(e)
            conn.send(b'Do math properly dumbo >:(\n')
            conn.close()


server = socketserver.ThreadingTCPServer(('0.0.0.0', 1337), AaaSHandler)

server.serve_forever()