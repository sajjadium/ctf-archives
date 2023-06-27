import os

from operator import xor
from functools import reduce, wraps
from hashlib import sha256
from hmac import HMAC, compare_digest
from json import dumps, loads

def read_json(prompt):
    return loads(input(prompt))

def write_json(dct):
    print(dumps(dct))

def decode_json(data):
    assert type(data) is dict
    res = {}
    for k, v in data.items():
        assert type(k) is str
        if type(v) is dict:
            res[k] = decode_json(v)
        else:
            assert type(v) is str
            if k.startswith('$'):
                res[k[1:]] = bytes.fromhex(v)
            else:
                res[k] = v
    return res

def encode_json(data, key: str=None):
    if type(data) is dict:
        res = dict((encode_json(v, k) for k, v in data.items()))
    elif type(data) is bytes:
        res = data.hex()
        if key:
            key = f"${key}"
    else:
        assert type(data) is str, f"type must be dict|str|bytes not {type(data)}"
        res = data
    if key is None:
        return res
    return key, res

def hash_content(data, ctx: str = ''):
    if type(data) is dict:
        v : int = reduce(xor, (hash_content(v, f'{ctx}.{k}' if ctx else k) for k, v in data.items()), 0)
        return v
    elif type(data) is str:
        data = data.encode()
    assert type(data) is bytes, "must be bytes"
    return int.from_bytes(sha256(ctx.encode() + b'\x00' + data).digest(), 'big')

KEY = os.urandom(32)
FLAG = os.getenv("FLAG")

def tag(data: dict):
    assert type(data) is dict, "data must be a dict"
    res : int = hash_content(data)
    return HMAC(KEY, res.to_bytes(32, 'big'), sha256).digest()

def get_and_delete(data: dict, key: str):
    assert key in data, f"{key} required - was not found"
    val = data[key]
    del data[key]
    return val

def authenticate(data: dict):
    user_tag =  get_and_delete(data, 'tag')
    return compare_digest(user_tag, tag(data))

def auth_helper(require_auth: bool, f):
    @wraps(f)
    def wrapper(auth_ok: bool, /, **kwds):
        assert not require_auth or auth_ok, "authentication failure - bad tag"
        return f(**kwds)
    wrapper.require_auth = require_auth
    return wrapper

COMMANDS = {}

def command(require_auth=False):
    def decorator(f):
        COMMANDS[f.__name__] = auth_helper(require_auth, f)
        return f
    return decorator

def process_command(user_command):
    auth = False
    if 'tag' in user_command:
        auth = authenticate(user_command)
    cmd = get_and_delete(user_command, 'command')
    return COMMANDS[cmd](auth, **user_command)

@command()
def get_tag(*, cmd: str, data: dict):
    assert cmd in COMMANDS, f'unknown command "{cmd}"'
    assert not COMMANDS[cmd].require_auth, 'requested tag for authenticated command - denied!'
    data['command'] = cmd
    data['tag'] = tag(data)
    return data

@command()
def greet(*, name: str):
    return f'Greeting {name}!'

@command(True)
def get_flag():
    return FLAG

@command(True)
def exec(*, cmd, args, **kwds):
    assert type(args) is dict, "'args' must be a dict"
    return COMMANDS[cmd](True, **args)

running = [True]

@command()
def quit():
    running.pop()
    return "Bye!"

def main():
    print("All your base are belong to us!")
    while running:
        try:
            user_input = decode_json(read_json("What is your request? "))
            result = process_command(user_input)
            if result:
                write_json(encode_json(result))
        except Exception as e:
            write_json({"error": str(e)})

if __name__ == "__main__":
    main()