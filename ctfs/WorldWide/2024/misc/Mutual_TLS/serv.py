import ssl
from OpenSSL import crypto
from flask import Flask, request
from werkzeug.serving import WSGIRequestHandler, make_server

app = Flask(__name__)


def extract_subject_from_cert(ssl_socket):
    try:
        for cert in ssl_socket.get_unverified_chain():
            cert = cert
        cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)
        subject = cert.get_subject().CN
        return subject.strip()
    except Exception as e:
        return ''


class CustomRequestHandler(WSGIRequestHandler):

    def make_environ(self):
        environ = super().make_environ()
        environ['subject'] = self.subject
        return environ

    def run_wsgi(self):
        ssl_socket = self.connection
        self.subject = extract_subject_from_cert(ssl_socket)
        super().run_wsgi()


@app.route("/")
def home():
    subject = request.environ.get('subject', [])
    print(subject)

    if subject == 'client.local':
        return "Hello user!\n", 200

    if subject == 'admin.local':
        return "Congrats! Here is the flag: wwf{REDACTED}\n", 200
    
    return "Invalid client certificate provided.\n", 401


if __name__ == "__main__":

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile="certs/server-cert.pem", keyfile="certs/server-key.pem")
    context.load_verify_locations(cafile="certs/ca-cert.pem")

    server = make_server("0.0.0.0", 443, app, request_handler=CustomRequestHandler, ssl_context=context)
    server.serve_forever()