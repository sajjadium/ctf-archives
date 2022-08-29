import random
import json
import pickle
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote_plus
from jinja2 import Environment


pickles = {}

env = Environment()


class PickleFactoryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("templates/index.html", "r") as f:
                self.wfile.write(f.read().encode())
            return
        elif parsed.path == "/view-pickle":
            params = parsed.query.split("&")
            params = [p.split("=") for p in params]
            uid = None
            filler = "##"
            space = "__"
            for p in params:
                if p[0] == "uid":
                    uid = p[1]
                elif p[0] == "filler":
                    filler = p[1]
                elif p[0] == "space":
                    space = p[1]
            if uid == None:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("No uid specified".encode())
                return
            if uid not in pickles:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(
                    "No pickle found with uid {}".format(uid).encode())
                return
            large_template = """
    <!DOCTYPE html>
    <html>
        <head>
            <title> Your Pickle </title>
            <style>
                html * {
                    font-size: 12px;
                    line-height: 1.625;
                    font-family: Consolas; }
            </style>
        </head>
        <body>
            <code> """ + str(pickles[uid]) + """ </code>
            <h2> Sample good: </h2>
            {% if True %}
            {% endif %}
            {{space*59}}
            {% if True %}
            {% endif %}
            {{space*6+filler*5+space*48}}
            {% if True %}
            {% endif %}
            {{space*4+filler*15+space*27+filler*8+space*5}}
            {% if True %}
            {% endif %}
            {{space*3+filler*20+space*11+filler*21+space*4}}
            {% if True %}
            {% endif %}
            {{space*3+filler*53+space*3}}
            {% if True %}
            {% endif %}
            {{space*3+filler*54+space*2}}
            {% if True %}
            {% endif %}
            {{space*2+filler*55+space*2}}
            {% if True %}
            {% endif %}
            {{space*2+filler*56+space*1}}
            {% if True %}
            {% endif %}
            {{space*3+filler*55+space*1}}
            {% if True %}
            {% endif %}
            {{space*3+filler*55+space*1}}
            {% if True %}
            {% endif %}
            {{space*4+filler*53+space*2}}
            {% if True %}
            {% endif %}
            {{space*4+filler*53+space*2}}
            {% if True %}
            {% endif %}
            {{space*5+filler*51+space*3}}
            {% if True %}
            {% endif %}
            {{space*7+filler*48+space*4}}
            {% if True %}
            {% endif %}
            {{space*9+filler*44+space*6}}
            {% if True %}
            {% endif %}
            {{space*13+filler*38+space*8}}
            {% if True %}
            {% endif %}
            {{space*16+filler*32+space*11}}
            {% if True %}
            {% endif %}
            {{space*20+filler*24+space*15}}
            {% if True %}
            {% endif %}
            {{space*30+filler*5+space*24}}
            {% if True %}
            {% endif %}
            {{space*59}}
            {% if True %}
            {% endif %}
        </body>
    </html>
"""
            try:
                res = env.from_string(large_template).render(
                    filler=filler, space=space)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(res.encode())
            except Exception as e:
                print(e)
                self.send_response(500)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("Error rendering template".encode())
            return
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("Not found".encode())
            return

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/create-pickle":
            length = int(self.headers.get("content-length"))
            body = self.rfile.read(length).decode()
            try:
                data = unquote_plus(body.split("=")[1]).strip()
                data = json.loads(data)
                pp = pickle.dumps(data)
                uid = generate_random_hexstring(32)
                pickles[uid] = pp
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(uid.encode())
                return
            except Exception as e:
                print(e)
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("Invalid JSON".encode())
                return
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("Not found".encode())
            return


def render_template_string_sanitized(env, template, **args):
    # it works!
    global_vars = ['self', 'config', 'request', 'session', 'g', 'app']
    for var in global_vars:
        template = "{% set " + var + " = None %}\n" + template
    return env.from_string(template).render(**args)


def generate_random_hexstring(length):
    return "".join(random.choice("0123456789abcdef") for _ in range(length))


if __name__ == "__main__":
    PORT = 9229
    with HTTPServer(("", PORT), PickleFactoryHandler) as httpd:
        print(f"Listening on 0.0.0.0:{PORT}")
        httpd.serve_forever()
