#!/usr/bin/python -u

import os
import socket
import subprocess
import threading
import sys
from hashlib import md5
from contextlib import closing

sys.stderr = open('/tmp/log', 'wb', 0)

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        s.bind(('', 0))
        return s.getsockname()[1]

def client_checker():
    try:
        sys.stdin.read()
    finally:
        p.kill()

prefix = os.urandom(8).encode('hex')
suffix = raw_input('md5("%s" + input).startswith("00000") >> ' % prefix)
if md5(prefix + suffix).hexdigest().startswith('00000') or 1:
    print "Running server..."
    dirname = os.path.dirname(__file__)
    os.chdir(dirname)
    path = os.path.join(dirname, 'run.sh')
    print "Finding free port..."
    port = find_free_port()
    print "Your port:", port
    print "Guest runs daemon on port 8888, but it's redirected to the port above"

    # NOTE: ./main is in initramfs.cpio.gz

    argv="/usr/bin/qemu-system-arm", "-kernel", "zImage", "-cpu", "arm1176", "-m", "32", "-M", "versatilepb", "-no-reboot", \
        "-initrd", "initramfs.cpio.gz", "-append", \
        "root=/dev/ram0 elevator=deadline rootwait quiet nozswap nortc noswap console=ttyAMA0 noacpi acpi=off", \
        "-redir", "tcp:" + str(port) + "::8888", \
        "-nographic"

    try:
        p = subprocess.Popen(argv, env={}, stdin=open('/dev/null', 'rb'), stdout=subprocess.PIPE)
    except:
        import traceback
        traceback.print_exc()
        print "Launch failed! Please contact to administrator"
        exit()

    # Check if client's disconnected
    t = threading.Thread(target=client_checker)
    t.start()

    # Check if qemu's halted
    d = ''
    while True:
        x = p.stdout.read(1)
        if x == '':
            break
        try:
            sys.stdout.write(x)
        except IOError:
            p.kill()
            break
        d += x
        if 'System halted' in d:
            p.kill()
            break
