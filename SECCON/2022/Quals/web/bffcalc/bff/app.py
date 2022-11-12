import cherrypy
import time
import socket


def proxy(req) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("backend", 3000))
    sock.settimeout(1)

    payload = ""
    method = req.method
    path = req.path_info
    if req.query_string:
        path += "?" + req.query_string
    payload += f"{method} {path} HTTP/1.1\r\n"
    for k, v in req.headers.items():
        payload += f"{k}: {v}\r\n"
    payload += "\r\n"

    sock.send(payload.encode())
    time.sleep(.3)
    try:
        data = sock.recv(4096)
        body = data.split(b"\r\n\r\n", 1)[1].decode()
    except (IndexError, TimeoutError) as e:
        print(e)
        body = str(e)
    return body


class Root(object):
    indexHtml = open("index.html").read()

    @cherrypy.expose
    def index(self):
        return self.indexHtml

    @cherrypy.expose
    def default(self, *args, **kwargs):
        return proxy(cherrypy.request)


cherrypy.config.update({"engine.autoreload.on": False})
cherrypy.server.unsubscribe()
cherrypy.engine.start()
app = cherrypy.tree.mount(Root())
