#!/usr/bin/env python3

import os
import random
import subprocess
import time

DEBUG = os.environ.get("DEBUG", "0") == "1"

def drop_to_unprivileged(uid: int, gid: int):
    # Drop to a unprivileged user and group.
    assert uid != 0 and gid != 0
    os.setresgid(uid, uid, uid)
    os.setresuid(gid, gid, gid)

def drop_to_ctf_uid_gid():
    drop_to_unprivileged(4242, 4242)

(r, w) = os.pipe()
os.set_inheritable(w, True)

repl = subprocess.Popen(["./repl.py", str(w)], close_fds=False, preexec_fn=drop_to_ctf_uid_gid)

os.close(w)
ppipe = os.fdopen(r, "r", buffering=1)

allowed = {
    "ls": True,
}


try:
    while repl.poll() == None:
        cmd = ppipe.readline()
        if cmd == "":
            break

        cmd = cmd.strip().split(" ")
        if DEBUG:
            print("RECEIVED COMMAND:", cmd)

        if cmd[0] == "exit":
            break
        elif cmd[0] == "ls" and allowed["ls"] and len(cmd) == 2:
            valid = True
            resolved = []
            path = cmd[1]

            if not path.startswith("-") and os.path.isdir(path):
                cmd = ["ls", "-l", path]
                if DEBUG:
                    print(cmd)

                subprocess.run(cmd, stderr=(subprocess.STDOUT if DEBUG else subprocess.DEVNULL), preexec_fn=drop_to_ctf_uid_gid)

            allowed["ls"] = False
except Exception as ex:
    if DEBUG:
        import traceback
        traceback.print_exc()

if DEBUG:
    print("Terminating REPL process...")

repl.kill()
repl.wait()

if DEBUG:
    print("REPL terminated - waiting...")

time.sleep(random.randrange(300, 600))
