import os
import re
import sys
import time
import typing
import socket
import logging
import traceback
import multiprocessing

from . import utils
from .const import *

from jinja2 import Template
from rich import print as rich_print
from urllib.parse import parse_qs, unquote

from ._types import ObjDict, TruncatedStringHandler


#=========================
# INCREASE THESE VALUE IF
# THE CHALLENGE ISN'T WORKING
# CORRECTLY
MAX_REQ_SIZE = int(os.environ.get("MAX_REQ_SIZE", 16384))
SOCK_TIMEOUT = int(os.environ.get("SOCK_TIMEOUT", 5))
SHORT_SOCK_TIMEOUT = float(os.environ.get("SHORT_SOCK_TIMEOUT", .15))
WORKERS = int(os.environ.get("WORKERS", 4)) # Default value
# ========================
VERSION = "1.0"

BLOCK_RE = re.compile(r"([\S\s]+(?=\r\n\r\n))") # Matching HTTP header only
HEADER_RE = re.compile(r"([a-zA-Z-]{1,40})\:\s*(.{1,128})") # Matching headers (header: value)
PATH_TRAVERSAL_RE = re.compile(r"(^(\\|\/))|(\.\.(\/|\\))") # Matching path traversal patterns (/ | ../ | ..\)
CONTENT_LENGTH = re.compile(r"Content-Length:\s(\d+)") # Matching content-length header (only positive values)
PARSER_RE = re.compile(r"([\S\s]+)(?=(\r\n\r\n(.+))|(\r\n\r\n))") # Matching HTTP header and body

METHODS = [
    "GET",
    "POST"
]

ERRORS = {
    418: "I'm a teapot",
    500: "Internal Server Error",
    405: "Method Not Allowed",
    401: "Unauthorized",
    404: "Not found"
}

SUPPORTED_HTTP_VERSIONS = ["HTTP/1.1"]


class App:
    name: str
    is_main: bool
    __nworkers: int
    server: socket.socket
    endpoints: typing.Dict
    running: bool
    _shared: typing.Dict
    ratelimit: int
    def __init__(self, name, ratelimit=float(os.environ.get("RATELIMIT", "inf")), nworkers=WORKERS):
        self.endpoints = dict()
        self.name = name
        self.__nworkers = nworkers
        self.is_main = self.name == "__main__"
        self.ratelimit = ratelimit
        
    def get(self, endpoint: str, function: typing.Callable) -> None:
        if endpoint not in self.endpoints:
            self.endpoints[endpoint] = {"methods": {}}
            
        self.endpoints[endpoint]["methods"].update({
            "GET": function
        })
        
    def post(self, endpoint: str, function: typing.Callable) -> None:
        if endpoint not in self.endpoints:
            self.endpoints[endpoint] = {"methods": {}}
            
        self.endpoints[endpoint]["methods"].update({
            "POST": function
        })
        
    def stop(self) -> None:
        sys.exit(0)
        
    def run(self, address: str="0.0.0.0", port: int=80) -> None:
        if self.is_main:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.server.bind((address, port))
            self.server.listen(self.__nworkers * 2)
            self._shared = multiprocessing.Manager().dict()
            workers = [multiprocessing.Process(target=handler, args=(self.server, self, )) for _ in
                range(self.__nworkers)]

            for w in workers:
                w.daemon = True
                w.start()
        
            if address == "0.0.0.0":
                rich_print("[green] * Running on all addresses.[/green]")
            rich_print(f"[yellow] * Server started at[/yellow] http://localhost:{port}/\n")
                
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                rich_print("[yellow]Stopping all processes...[/yellow]")
                self.stop()
                
def set_logger() -> None:
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%H:%M:%S.%f]", handlers=[TruncatedStringHandler()]
    )
    
def set_status_code(ctx: ObjDict, status_code: int) -> None:
    ctx.response.status_code = status_code
    ctx.response.message = ERRORS.get(status_code, ERRORS[404])

def recvuntil(sock: socket.socket, 
              buffer_size: int=4096) -> typing.List:
    received_data = ""
    post_data = ""
    match = None
    
    sock.settimeout(SOCK_TIMEOUT)
    while not match:
        received_data += sock.recv(buffer_size).decode()
        assert received_data.count("\r") < 1024
        match = PARSER_RE.search(received_data[:MAX_REQ_SIZE]) # Receiving until \r\n\r\n found
        
    try:
        sock.settimeout(SHORT_SOCK_TIMEOUT)
        sock.recv(16, socket.MSG_PEEK) # Receiving without consuming
        if match:
            content = match.group(1)
            if (content_length := CONTENT_LENGTH.search(content)):
                content_length = int(content_length.group(1))
                post_data += sock.recv(content_length).decode() # Receiving POST data
            return PARSER_RE.search(content + post_data).groups()
    except TimeoutError:
        return match.groups()
    except AttributeError:
        pass

def render_template(template_file: str, **kwargs) -> str:
    with open(os.path.join(PUBLIC_DIR, "templates", template_file), 'r') as f:
        buf = f.read()
    return Template(buf).render(kwargs)

def parse_request(request: typing.List, ctx: ObjDict) -> None:
    ctx.response = ObjDict() 
    ctx.request = ObjDict()
    
    ctx.response.status_code = 200 # Default value
    ctx.response.message = "OK" # Default value
    ctx.response.headers = { # Static headers.
        "Server": f"Borraccia/{VERSION}",
        "Content-Type": "text/html", # Only html content is supported
        "Content-Security-Policy": "default-src 'none'; require-trusted-types-for 'script'",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    ctx.response.header = ""
    ctx.response.body = ""
    
    start_and_headers = request[0]
    should_be_a_post_request = bool(request[-2])
    post_data = request[-2]
    post_data = utils.extract_params(parse_qs(post_data) if post_data else {})
    
    rows = start_and_headers.split("\n")
    first_row = rows[0].split()
            
    method = first_row[0]
    path = first_row[1]

    params = utils.extract_params(parse_qs(params[1]) if len((params:=path.split("?"))) > 1 else {})
    
    http_version = first_row[2]
    
    ctx.request.http_version = http_version
    ctx.request.params = params
    ctx.request.path = unquote(path.split("?")[0].lower())
    ctx.request.post_data = post_data
    ctx.request.method = method
    
    assert method.isalpha()

    if method not in METHODS:
        ctx.response.status_code = 405 # Method not supported
    
    elif http_version not in SUPPORTED_HTTP_VERSIONS:
        ctx.response.status_code = 418 # I'm a teapot
    
    elif should_be_a_post_request:
        if not method == "POST":
            ctx.response.status_code = 500 # Internal Server Error

    elif PATH_TRAVERSAL_RE.search(uq:=unquote(path[1:])):
        ctx.response.status_code = 401 # Unauthorized
        utils.log(logging, f"Path traversal attempt detected ", "ERROR")

    for probable_header in filter(None, rows[1:]): # Memorizing headers
        if (cap:=HEADER_RE.search(probable_header)):
            header = cap.group(1)
            value = cap.group(2)

            h = utils.normalize_header(header)
            v = utils.normalize_header_value(value)
            ctx.request[h] = v 
             
def request_handler(client: socket.socket, 
                    address: typing.Tuple, 
                    app: App, 
                    curr: str) -> None:
    with ObjDict() as ctx:
        data = recvuntil(client)
        if not data:
            ctx.response.body = utils.serve_error(500)
            ctx.response.message = ERRORS[500]
            client.send((ctx.response.header + ctx.response.body).encode())
        
        parse_request(data, ctx) # Extract path, params, headers, etc...
        res = function_wrapper(app, ctx) # Check if the path is valid
        
        if ctx.response.status_code == 200:
            ctx.response.status_code = res
        
        if ctx.response.status_code != 200: # Something went wrong
            ctx.response.message = ERRORS.get(ctx.response.status_code, ERRORS[500])
            ctx.response.body = utils.serve_error(ctx.response.status_code)
        else:
            try:
                ctx.response.body = app.endpoints[ctx.request.path]["methods"][ctx.request.method](ctx)
            except Exception as e: # Something went wrong with App()
                utils.log(logging, ''.join(traceback.format_exception(e)[-2:]), "ERROR")
                ctx.response.body =  utils.serve_error(500) + utils.make_comment(f"{e}") 
                ctx.response.message = ERRORS[500]
        
        try:
            utils.build_header(ctx) # Now the response is ready to be sent
            utils.log(logging, f"[{curr}]\t{ctx.request.method}\t{ctx.response.status_code}\t{address[0]}", "DEBUG", ctx)    
            assert ctx.response.status_code in ERRORS or ctx.response.status_code == 200
        except AssertionError:
            raise # Something unexpected happened, close conection immediately
        except Exception as e:
            ctx.response.status_code = 500
            ctx.response.header = ""
            ctx.response.body = utils.serve_error(ctx.response.status_code) + utils.make_comment(f"{e}") # Something went wrong while building the header.
            utils.build_header(ctx)
            
        client.send((ctx.response.header + ctx.response.body).encode())

def function_wrapper(app: App, ctx: ObjDict) -> bool:
    return 200 if (endpoint:=app.endpoints.get(ctx.request.path)) and ctx.request.method in endpoint["methods"] else 404

def request_wrapper(client, address, app: App, curr): # This is beautiful!
    addr = address[0]
    if addr not in app._shared:
        app._shared[addr] = (time.time(), 0)

    app._shared[addr] = (app._shared[addr][0], app._shared[addr][1]+1)
    
    if time.time() - app._shared[addr][0] > 1*60:
        app._shared[addr] = (time.time(), 0)
        
    if app._shared[addr][1] < app.ratelimit:
        request_handler(client, address, app, curr)

def handler(sock: socket.socket, app: App) -> None:
    curr = multiprocessing.current_process().name.split("-")[-1]
    set_logger()

    while True:
        try:
            client, address = sock.accept()
            request_wrapper(client, address, app, curr)
        except Exception as e:
            utils.log(logging, f"[{curr}] [{address[0]}:{address[1]}] {e}", "ERROR")
        client.close()

