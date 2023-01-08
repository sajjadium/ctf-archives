#!/usr/bin/env python3

import os
import sys
import base64
import tempfile
# pip install qiling==1.4.1
from qiling import Qiling

def my_sandbox(path, rootfs):
    ql = Qiling([path], rootfs)
    ql.run()

def main():
    sys.stdout.write('Your Binary(base64):\n')
    line = sys.stdin.readline()
    binary = base64.b64decode(line.strip())
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        fp = os.path.join(tmp_dir, 'bin')

        with open(fp, 'wb') as f:
            f.write(binary)

        my_sandbox(fp, tmp_dir)

if __name__ == '__main__':
    main()
