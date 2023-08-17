import requests, argparse, os
from http.server import HTTPServer, BaseHTTPRequestHandler


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        if not self.headers["Cookie"] or "flag=" not in self.headers["Cookie"]:
            self.send_header('Set-Cookie', "flag=ALLES!{redacted}")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>Tickets</h1>{message}</body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        if os.environ["TICKET_APP_API"]:
            burp0_url = os.environ["TICKET_APP_API"]
        else:
            burp0_url = "http://localhost:4000/"
        burp0_headers = {"sec-ch-ua": "\"-Not.A/Brand\";v=\"8\", \"Chromium\";v=\"102\"", "sec-ch-ua-mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36", "sec-ch-ua-platform": "\"Windows\"", "Content-Type": "application/json", "Accept": "*/*", "Origin": "https://lucasconstantino.github.io", "Sec-Fetch-Site": "cross-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Accept-Encoding": "gzip, deflate", "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "close"}
        burp0_json={"query": "query { tickets {\n  id\n  issue\n  __typename\n}}\n", "variables": None}
        response = requests.post(burp0_url, headers=burp0_headers, json=burp0_json)
        res = response.json()
        if res["data"]["tickets"]:
            body = "<ul>\n"
            for ticket in res["data"]["tickets"]:
                body += "\t<li>" + ticket["issue"] + "</li>\n"
            body+="</ul>"
        else:
            body = "<h2>No Tickets yet</h2>"
        self.wfile.write(self._html(body))

    def do_HEAD(self):
        self._set_headers()

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
