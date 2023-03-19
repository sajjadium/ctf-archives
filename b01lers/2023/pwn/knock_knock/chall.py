import base64
from subprocess import Popen, PIPE
import struct
import shutil
import uuid
import os
import sys

MAX_CODE_SIZE = 4096 * 4

def main():
    if len(sys.argv) == 2:
        # use user supplied file
        with open(sys.argv[1], 'rb') as f:
            data = f.read()
    else:
        code = input('Enter base 64 encoded machine code: ')

        try:
            data = base64.b64decode(code)
        except:
            print('invalid base64 encoded data')
            return

    if len(data) > MAX_CODE_SIZE:
        print('Code is too long')
        return
    
    size_bytes = struct.pack('<H', len(data))

    disk_uuid = uuid.uuid4()
    disk_name = f'/tmp/{disk_uuid}'
    shutil.copy('disk_redacted.img', disk_name)

    try:
        with Popen([
            'timeout', '5',
            'qemu-system-x86_64',
            '-m', '512M',
            '-serial', 'stdio',
            '-drive', f'file={disk_name},format=raw',
            '-display', 'none',
            '-monitor', 'none',
            '-no-reboot',
        ], stdout=PIPE, stdin=PIPE) as p:
            # For some reason, the first byte is ignored
            p.stdin.write(b'\0')
            p.stdin.write(size_bytes)
            p.stdin.write(data)

            p.stdin.flush()

            print(p.stdout.read().decode('ascii'))
    except:
        print('timeout')
    
    os.remove(disk_name)

if __name__ == '__main__':
    main()