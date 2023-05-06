#!/usr/bin/python3 -EIs

"""
Give a different UID to each SSH connection.

Not meant to be secure, just prevent different users from messing with each
other (there is nothing to see here.)
"""

import logging
import os
import re
import shutil
import sys

MIN_UID = 3000
MAX_UID = 3100
WORKDIR = "/tmp/ghostbuster"

def drop_privileges(uid, gid):
    os.setgroups([])
    os.setgid(gid)
    os.setuid(uid)
    os.umask(0o77)

def remove_user(uid):
    logger.info(f"removing user {uid}")
    shutil.rmtree(f"{WORKDIR}/{uid}/")
    os.remove(f"{WORKDIR}/{uid}.user")

def create_user(uid, gid, ssh_connection):
    logger.info(f"adding user {uid}")

    # raises an FileExistsError if the file already exists
    with open(f"{WORKDIR}/{uid}.user", "x") as fp:
        fp.write(ssh_connection)

    tmpdir = f"{WORKDIR}/{uid}"
    os.makedirs(tmpdir, 0o700, True)
    os.chown(tmpdir, uid, gid)

def reuse_connection(connected, ssh_connection):
    for dirname in os.listdir(WORKDIR):
        if not re.match("^[0-9]+\.user$", dirname):
            continue

        uid = int(os.path.splitext(dirname)[0])

        # remove disconnected users
        if uid not in connected:
            remove_user(uid)
            continue

        with open(f"{WORKDIR}/{uid}.user") as fp:
            connection = fp.read()
        if connection == ssh_connection:
            logger.info(f"reusing connection {ssh_connection} for uid {uid}")
            return uid

    return -1

def pick_user(connected, ssh_connection):
    """Pick an available user"""

    uids = set(range(MIN_UID, MAX_UID)) - set(connected)
    if not uids:
        logger.error("no uid available")
        sys.exit(1)

    uid = sorted(uids)[0]
    try:
        create_user(uid, uid, ssh_connection)
    except FileExistsError:
        connected.append(uid)
        return pick_user(connected, ssh_connection)

    return uid

def connected_uids():
    """Return a list of connected users."""

    # walk /proc/ to retrieve running processes
    uids = set([])
    for pid in os.listdir("/proc/"):
        if not re.match("^[0-9]+$", pid):
            continue

        try:
            uid = os.stat(f"/proc/{pid}").st_uid
        except FileNotFoundError:
            continue

        if uid in range(MIN_UID, MAX_UID):
            uids.add(uid)

    return list(uids)

def new_connection(ssh_connection):
    connected = connected_uids()
    logger.info(f"connected users: {connected}")

    uid = reuse_connection(connected, ssh_connection)
    if uid == -1:
        uid = pick_user(connected, ssh_connection)

    drop_privileges(uid, gid=uid)

    tmpdir = f"{WORKDIR}/{uid}"
    os.chdir(tmpdir)

    os.putenv("HOME", "/home/ghostbuster")
    os.putenv("USER", "ghostbuster")
    try:
        os.symlink("/home/ghostbuster/challenge.sh", os.path.join(tmpdir, "challenge.sh"))
    except FileExistsError:
        pass

    if "SSH_ORIGINAL_COMMAND" in os.environ:
        args = [ "bash", "-c", os.environ["SSH_ORIGINAL_COMMAND"] ]
    else:
        args = [ "bash" ]

    logger.info(f"executing {args}")
    os.execv("/bin/bash", args)

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger("ssh-isolation")

    if not os.path.exists(WORKDIR):
        os.mkdir(WORKDIR, 0o711)

    if "SSH_CONNECTION" not in os.environ:
        logger.critical("environment variable SSH_CONNECTION is not set")
        sys.exit(1)

    new_connection(os.environ["SSH_CONNECTION"])
