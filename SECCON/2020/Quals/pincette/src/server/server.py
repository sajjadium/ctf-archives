#!/usr/bin/env python3
import subprocess
import tempfile
import sys
import shutil
import base64
import os
import pwd
import grp
import signal

ORIGINAL_LIBC = '/lib/x86_64-linux-musl/libc.so'
PIN_PATH = '/opt/pin/pin'
PINCETTE_DIR = '/opt/pincette'
DIRNAME_PREFIX = 'lib_'
IBT_PATH = '/opt/pincette/ibt.so'

def drop_privileges():
    os.setgid(grp.getgrnam('nogroup').gr_gid)
    os.setuid(pwd.getpwnam('nobody').pw_uid)

def timeout(signum, frame):
    raise IOError

def main():
    signal.signal(signal.SIGALRM, timeout)
    os.chdir(PINCETTE_DIR)
    with tempfile.TemporaryDirectory(prefix=DIRNAME_PREFIX, dir=PINCETTE_DIR) as dirname:
        # get user input
        signal.alarm(10)
        baseaddr = int(input('Enter baseaddr of libc: '), 0)
        payload = base64.decodebytes(input("Enter base64 payload: ").encode())
        signal.alarm(0)

        # make copy of libc
        os.chmod(dirname, 0o755)
        shutil.copy(ORIGINAL_LIBC, dirname);

        # modify baseaddr of libc
        rslt = subprocess.run(
            ['/usr/sbin/prelink', '-r', '0x%x' % baseaddr,dirname+'/libc.so'],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        if rslt.returncode != 0:
            sys.stdout.write(rslt.stdout.decode())
            sys.exit(-1)

        # execute vuln with modified libc
        env = { 'LD_LIBRARY_PATH': dirname, 'LD_USE_LOAD_BIAS': '1'}
        cmdline = [ "timeout", "-sKILL", "10",
            PIN_PATH, '-logfile', '', '-t', IBT_PATH, '-logfile', '', '--', '/opt/pincette/vuln']
        rslt = subprocess.run(cmdline, input=payload, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, env=env, preexec_fn=drop_privileges, start_new_session=True)
        sys.stdout.write(rslt.stdout.decode())

if __name__ == '__main__':
    main()
