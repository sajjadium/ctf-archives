#!/usr/bin/env python3.10
import dis
import os
import sys
import re
import runpy
import py_compile

import requests


PLUGINS_PATH = "/plugins/"
TRUSTED_DOMAINS = [
    'blackhat.day',
    'veganrecipes.soy',
    'fizzbuzz.foo',
]

def banner():
    print("1. List known websites")
    print("2. List plugins")
    print("3. Download plugin")
    print("4. Load plugin")
    print("5. Exit")

def list_known_websites():
    print("great.veganrecipes.soy")
    print("uplink.blackhat.day")
    print("plugandplay.fizzbuzz.foo")

def list_plugins():
    print("Plugins:")
    for f in os.listdir(PLUGINS_PATH):
        print(f"  {f}")


PATH_RE = re.compile(r"^[A-Za-z0-9_]+$")
MAX_SIZE = 4096

def _get_file(url):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        chunks = 0
        for chunk in r.iter_content(chunk_size=4096): 
            return chunk
    raise Exception("")


def download_plugin():
    print("Provide plugin url in a form of A.B.C where A,B,C must be [A-Za-z0-9_]+")
    url = input("url: ").strip()
    try:
        a, b, c = url.split(".")
        if not all(PATH_RE.match(x) for x in (a, b, c)):
            print("FAIL:",a,b,c)
            raise Exception()
    except:
        print("ERR: Invalid url format. Cannot download plugin.")
        return

    domain = f"{b}.{c}"
    if domain not in TRUSTED_DOMAINS:
        print("ERR: Domain not trusted. Aborting.")
        return

    url = f"https://{a}.{b}.{c}/"
    try:
        code = _get_file(url).decode()
        # Validate plugin code
        cobj = test_expr(code, ALLOWED_OPCODES)
        # Constants must be strings!
        assert all(type(c) in (str, bytes, type(None)) for c in cobj.co_consts)
    except Exception as e:
        print(f"ERR: Couldnt get plugin or plugin is invalid. Aborting.")
        return

    # TODO/FIXME: So far our plugins will just print global strings
    # We should make it more powerful in the future, but at least it is secure for now
    code += '\nx = [i for i in globals().items() if i[0][0]!="_"]\nfor k, v in x: print(f"{k} = {v}")'

    with open(f"{PLUGINS_PATH}/{a}_{b}.py", "w") as f:
        f.write(code)

### Code copied from Pwntools safeeval lib
# see https://github.com/Gallopsled/pwntools/blob/c72886a9b9/pwnlib/util/safeeval.py#L26-L67
# we did a small modification: we pass 'exec' instead of 'eval' to `compile`
def _get_opcodes(codeobj):
    if hasattr(dis, 'get_instructions'):
        return [ins.opcode for ins in dis.get_instructions(codeobj)]
    i = 0
    opcodes = []
    s = codeobj.co_code
    while i < len(s):
        code = six.indexbytes(s, i)
        opcodes.append(code)
        if code >= dis.HAVE_ARGUMENT:
            i += 3
        else:
            i += 1
    return opcodes

def test_expr(expr, allowed_codes):
    allowed_codes = [dis.opmap[c] for c in allowed_codes if c in dis.opmap]
    try:
        c = compile(expr, "", "exec")
    except SyntaxError:
        raise ValueError("%r is not a valid expression" % expr)
    codes = _get_opcodes(c)
    for code in codes:
        if code not in allowed_codes:
            raise ValueError("opcode %s not allowed" % dis.opname[code])
    return c


ALLOWED_OPCODES = ["LOAD_CONST", "STORE_NAME", "RETURN_VALUE"]

def load_plugin():
    """
    Loads the plugin performing various sanity checks.
    A plugin must only define strings in it.
    """
    plugin = input("plugin: ").strip()
    if not PATH_RE.match(plugin):
        print("Invalid plugin name. Aborting.")
        return

    plugin_path = f"{PLUGINS_PATH}/{plugin}.py"

    if not os.path.exists(plugin_path):
        print("Path not found: %s" % plugin_path)
        return

    # We validated the plugin when we downloaded it
    # so it must be secure to run it now: it should just print globals.
    runpy.run_path(py_compile.compile(plugin_path))

funcs = {
    1: list_known_websites,
    2: list_plugins,
    3: download_plugin,
    4: load_plugin,
    5: sys.exit
}

def main():
    print("Welcome to the PyPlugins challenge!")
    print("We will load your Python plugins, but only if they are hosted on a trusted website and if they cannot harm us.")
    
    while True:
        banner()
        n = input('> ')
        try:
            n = int(n)
            func = funcs[n]
        except:
            print("Wrong input. Try again")
            continue
        try:
            func()
        except Exception as e:
            print(f"Faild")
            raise

if __name__ == '__main__':
    main()
