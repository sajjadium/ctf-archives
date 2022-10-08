import http.server
from socketserver import ThreadingMixIn
from subprocess import run
import re

AES_KEY_WHITELIST = r"^[A-Z0-9]{32}$"
AES_KEY_HEADER = "X-AES-KEY"

class ApiHandler(http.server.BaseHTTPRequestHandler):
    
    def read_body(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)
        return body


    def do_cli(self, cmd):
        content = self.read_body()

        output = run(
            cmd,
            capture_output=True,
            input=content, 
            shell=True
        ).stdout

        self.send_response(200)
        self.end_headers()
        self.wfile.write(output)

    
    def do_decrypt(self):
        self.do_cli("xxd -r -p|openssl enc -d -aes-128-ecb  -K {}".format(self.headers[AES_KEY_HEADER]))
    
    def do_encrypt(self):
        self.do_cli("openssl enc -aes-128-ecb  -K {}|xxd -p".format(self.headers[AES_KEY_HEADER]))

    def do_POST(self):
        aes_key = self.headers.get('X-AES-KEY', "")
        if re.match(AES_KEY_WHITELIST, aes_key):
            if self.path.startswith("/encrypt"):
                self.do_encrypt()
            elif self.path.startswith("/decrypt"):
                self.do_decrypt()
            else:
                self.send_error(501, "Not supported.")
        else:
            self.send_error(400, "Invalid AES key.")


class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    pass

server = ThreadedHTTPServer(("0.0.0.0", 1337), ApiHandler)
server.serve_forever()