from server import decrypt, generate_new_auth_token
import socket, signal, json, threading
from socketserver import BaseRequestHandler, TCPServer, ForkingMixIn


address = ('0.0.0.0', 11223)


class ChallengeHandler(BaseRequestHandler):
    def challenge(self, req, verifier, verify_counter):
        authtoken = req.recv(1024).decode().strip()
        ret = decrypt(authtoken, verifier, verify_counter)
        req.sendall(json.dumps(ret).encode('utf-8')+b'\n')

    def handle(self):
        signal.alarm(1500)
        req = self.request
        req.settimeout(60)

        new_auth_token, verifier = generate_new_auth_token()
        req.sendall(b"Leaked Token:"+new_auth_token.hex().encode('utf-8')+b"\n")
        verify_counter = 0
        while True:
            try:
                self.challenge(req, verifier, verify_counter)
            except socket.timeout as e:
                req.sendall(b"Timeout. Bye.\n")
                break
            except socket.error:
                break
            except Exception as e:
                print(e)
                break
            finally:
                if verify_counter < 2:
                    verify_counter+=1

class ChallengeServer(ForkingMixIn, TCPServer):
    request_queue_size = 100

    # For address reassignment on reboot
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)


if __name__ == "__main__":
    TCPServer.allow_reuse_address = True
    server = ChallengeServer(address, ChallengeHandler)
    server.serve_forever()
    
    with server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        while True:
            pass
        