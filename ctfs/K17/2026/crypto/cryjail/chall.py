#!/usr/bin/env python3
import ctypes
import os
import sys
import warnings

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


warnings.simplefilter("ignore")

KEY = get_random_bytes(16)
SAFE = set(range(0x20, 0x7F))  # printable ASCII, including '"' (0x22) and '\' (0x5c)
RUN_PATH = "/tmp/run.py"


def escape(data: bytes) -> str:
    out = []
    for c in data:
        out.append(chr(c) if c in SAFE else "\\x%02x" % c)
    return "".join(out)


# ---------------------------------------------------------------------------
# Landlock: restrict the whole process (and its forked children) to read-only
# filesystem access, except writing to the one scratch source file.
# ---------------------------------------------------------------------------
_libc = ctypes.CDLL(None, use_errno=True)
_NR = {"create": 444, "add": 445, "restrict": 446}  # x86-64 == arm64 for these
_PR_SET_NO_NEW_PRIVS = 38
_O_PATH = 0o10000000
_O_CLOEXEC = 0o2000000
# (ABI that introduced it, bit)
_FS_BITS = [(1, 1 << i) for i in range(13)] + [(2, 1 << 13), (3, 1 << 14), (4, 1 << 15)]
_FS_READ = (1 << 0) | (1 << 2) | (1 << 3)  # EXECUTE | READ_FILE | READ_DIR
_FS_WRITE = (1 << 1) | (1 << 14)  # WRITE_FILE | TRUNCATE


class _RulesetAttr(ctypes.Structure):
    _fields_ = [("handled_access_fs", ctypes.c_uint64)]


class _PathBeneath(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("allowed_access", ctypes.c_uint64), ("parent_fd", ctypes.c_int32)]


def _syscall(num, *args):
    res = _libc.syscall(ctypes.c_long(num), *args)
    if res < 0:
        err = ctypes.get_errno()
        raise OSError(err, os.strerror(err))
    return res


def _add_rule(ruleset_fd, path, access):
    fd = os.open(path, _O_PATH | _O_CLOEXEC)
    pb = _PathBeneath(allowed_access=access, parent_fd=fd)
    _syscall(_NR["add"], ctypes.c_int(ruleset_fd), ctypes.c_int(1),
             ctypes.byref(pb), ctypes.c_uint32(0))
    os.close(fd)


def lock_down(writable_paths):
    """Enforce read-only filesystem, allowing writes only to `writable_paths`."""
    abi = _libc.syscall(ctypes.c_long(_NR["create"]), None, ctypes.c_size_t(0),
                        ctypes.c_uint32(1))
    if abi <= 0:
        raise OSError("landlock unavailable (abi=%d)" % abi)
    handled = 0
    for since, bit in _FS_BITS:
        if since <= abi:
            handled |= bit
    attr = _RulesetAttr(handled_access_fs=handled)
    ruleset_fd = _syscall(_NR["create"], ctypes.byref(attr),
                          ctypes.c_size_t(ctypes.sizeof(attr)), ctypes.c_uint32(0))
    _add_rule(ruleset_fd, "/", handled & _FS_READ)
    for path in writable_paths:
        _add_rule(ruleset_fd, path, handled & _FS_WRITE)
    if _libc.prctl(_PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
        err = ctypes.get_errno()
        raise OSError(err, "prctl(NO_NEW_PRIVS): " + os.strerror(err))
    _syscall(_NR["restrict"], ctypes.c_int(ruleset_fd), ctypes.c_uint32(0))
    os.close(ruleset_fd)


# ---------------------------------------------------------------------------
# I/O helpers. We read control input UNBUFFERED from fd 0 so we never swallow
# bytes meant for a child process's own input().
# ---------------------------------------------------------------------------
def read_line() -> bytes:
    buf = bytearray()
    while True:
        c = os.read(0, 1)
        if not c:
            raise EOFError
        if c == b"\n":
            return bytes(buf)
        buf += c


def prompt(text: str):
    sys.stdout.write(text)
    sys.stdout.flush()


def build_program(name: bytes) -> str:
    return (
        "import os\n"
        'devnull = os.fdopen(os.open("/dev/null", os.O_WRONLY), "w")\n'
        'print(b"IMPLANTING NEURO LINK CHIP IN INDIVIDUAL IDENTIFIYING AS: ' + escape(name) + '!", file=devnull)\n'
    )


def run_child():
    try:
        with open(RUN_PATH) as f:
            code = compile(f.read(), RUN_PATH, "exec")
        exec(code, {"__name__": "__main__"})
        rc = 0
    except SystemExit as e:
        rc = e.code if isinstance(e.code, int) else 0
    except BaseException:
        rc = 1
    try:
        sys.stdout.flush()
    except Exception:
        pass
    os._exit(rc)


def main():
    open(RUN_PATH, "w").close()
    lock_down([RUN_PATH, "/dev/null"])

    print("== Mass Surveillance ==", flush=True)
    print("Hello operator, please send us the encrypted names of every person you've reconnaissanced so far.", flush=True)
    print(flush=True)

    while True:
        try:
            prompt("New name (iv:ciphertext, in hex): ")
            line = read_line()
        except EOFError:
            break

        try:
            iv_hex, ct_hex = line.split(b":", 1)
            iv = bytes.fromhex(iv_hex.decode())
            ct = bytes.fromhex(ct_hex.decode())
        except (ValueError, UnicodeDecodeError):
            print("[!] send hex as iv:ciphertext", flush=True)
            continue
        if len(iv) != 16:
            print("[!] the iv must be exactly 16 bytes", flush=True)
            continue
        if len(ct) == 0 or len(ct) % 16 != 0:
            print("[!] the ciphertext must be a non-empty multiple of 16 bytes",
                  flush=True)
            continue

        name = AES.new(KEY, AES.MODE_CBC, iv).decrypt(ct)
        program = build_program(name)
        fd = os.open(RUN_PATH, os.O_WRONLY | os.O_TRUNC)
        os.write(fd, program.encode())
        os.close(fd)

        sys.stdout.flush()
        pid = os.fork()
        if pid == 0:
            run_child()  # never returns
        _, status = os.waitpid(pid, 0)
        crashed = not (os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0)
        print("[!] probably not enough cores or something idk lmao" if crashed
              else "[ok] reported name to our database", flush=True)


if __name__ == "__main__":
    main()
