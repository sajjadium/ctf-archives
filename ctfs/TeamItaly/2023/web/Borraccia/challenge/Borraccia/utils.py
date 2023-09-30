import os
import re
import typing
from . import _types
from functools import lru_cache
from .const import STATIC_DIR, ERROR_DIR


@lru_cache
def normalize_header(s: str) -> str:
    return s.lower().replace('-', '_')

@lru_cache
def normalize_header_value(s: str) -> str:
    return re.sub(r"[%\"\.\n\'\!:\(\)]", "", s)

@lru_cache
def serve_file(path: str) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ''
    
@lru_cache
def serve_static_file(path: str) -> str:
    try:
        with open(resolve_path(STATIC_DIR, path), "r") as f:
            return f.read()
    except FileNotFoundError:
        return ''
    
@lru_cache
def serve_error(status_code: int) -> str:
    try:
        with open(resolve_path(ERROR_DIR, str(status_code).strip()), "r") as f:
            return f.read()
    except FileNotFoundError:
        return ''

def extract_params(p) -> typing.Dict:
    return {key: value[0] if isinstance(value, list) and len(value) == 1 else value \
        for key, value in p.items()}

@lru_cache
def resolve_path(base: str, path: str) -> str:
    return os.path.join(base, path) if ".." not in path else ''

def make_comment(s):
    return "<!--" + s + "-->"

def log(log, s, mode="INFO", ctx=None):
    {
        "DEBUG": log.debug,
        "INFO": log.info,
        "ERROR": log.error
    }[mode](s.format(ctx), {"mode": mode})

def build_header(ctx: _types.ObjDict) -> None: # Build the header with status code, headers, etc...
    ctx.response.header += ctx.request.http_version + " " + str(ctx.response.status_code) + " " + ctx.response.message + "\n"
    
    for header in ctx.response.headers:
        ctx.response.header += f"{header}: {ctx.response.headers[header]}\n"
        
    ctx.response.header += f"Content-Length: {len(ctx.response.body)}\n"

    ctx.response.header += "\n"
    ctx.response.header = ctx.response.header.replace("\n", "\r\n")

