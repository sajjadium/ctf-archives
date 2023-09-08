from pyamf.remoting.gateway.wsgi import WSGIGateway
import secrets

ADMIN_USER = secrets.token_urlsafe(16)
ADMIN_PASS = secrets.token_urlsafe(16)


class FileManagerService:
    def read(self, filename):
        with open(filename, "rb") as f:
            return f.read()

    def list(self, path="/"):
        import os

        return os.listdir(path)


def auth(username, password):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return True

    return False


gateway = WSGIGateway({"file_manager": FileManagerService}, authenticator=auth)


if __name__ == "__main__":
    from wsgiref import simple_server

    host = "0.0.0.0"
    port = 5000

    httpd = simple_server.WSGIServer((host, port), simple_server.WSGIRequestHandler)
    httpd.set_app(gateway)

    print("Running Authentication AMF gateway on http://%s:%d" % (host, port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
