#!/usr/bin/env python3

import io, os, re, sys, tarfile, importlib.util, signal

OCTAL_RE = re.compile(r'^[0-7]+$')

def to_bytes_from_octal_triplets(s: str) -> bytes:
    if not OCTAL_RE.fullmatch(s):
        sys.exit("invalid: only octal digits 0-7")
    if len(s) % 3 != 0:
        sys.exit("invalid: length must be multiple of 3")
    if len(s) > 300000:
        sys.exit("too long")
    return bytes(int(s[i:i+3], 8) for i in range(0, len(s), 3))

def safe_extract(tf: tarfile.TarFile, path: str):
    def ok(m: tarfile.TarInfo):
        name = m.name
        return not (name.startswith("/") or ".." in name)
    for m in tf.getmembers():
        if ok(m):
            tf.extract(m, path)

def load_and_run_plugin():
    for candidate in ("uploads/plugin.py", "plugin.py"):
        if os.path.isfile(candidate):
            spec = importlib.util.spec_from_file_location("plugin", candidate)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "run"):
                return mod.run()
            break
    print("No plugin found.")

def timeout(*_): sys.exit("timeout")
signal.signal(signal.SIGALRM, timeout)
signal.alarm(6)

print("Send octal")
data = sys.stdin.readline().strip()
blob = to_bytes_from_octal_triplets(data)

bio = io.BytesIO(blob)
try:
    with tarfile.open(fileobj=bio, mode="r:*") as tf:
        os.makedirs("uploads", exist_ok=True)
        safe_extract(tf, "uploads")
except Exception as e:
    sys.exit(f"bad archive: {e}")

load_and_run_plugin()
