import os
import string
import asyncio

def check_filename(fname):
    for c in fname:
        if c not in string.ascii_lowercase + "." + "/":
            return False
    return True

def get_content(fname: str | None) -> str:
    if fname:
        if not fname.endswith(".txt") or not check_filename(fname) or '../' in fname:
            return "can't do!"

        try:
            with open(fname, "r") as f:
                return f.read()
        except:
            return "error occured, not found?"
    return ""

async def get_filelist():
    if os.name == "nt":
        cmd = "dir"
    else:
        cmd = "ls"

    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, _ = await proc.communicate()
    return stdout.decode()


