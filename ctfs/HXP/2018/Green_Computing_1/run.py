#!/usr/bin/env python3
import random
import string
import sys
import tempfile
import shutil
import os
import base64

# Damn Chinese nation-state-level hackers added a tiny chip here :/
# Seems like they are injecting ACPI tables to save electricity O_O
# Please inform Bloomberg
tmp_dir = tempfile.mkdtemp(prefix='green_computing_', dir='/tmp')
os.chdir(tmp_dir)
os.makedirs('kernel/firmware/acpi')

with open('kernel/firmware/acpi/dsdt.aml', 'wb') as f:
	b = base64.b64decode(sys.stdin.readline(32 * 1024).strip())
	if b[:4] != b'DSDT':
		b = b''
	f.write(b)

os.system('find kernel | cpio -H newc --create --owner 0:0 > tables.cpio')
os.system('cat tables.cpio /home/ctf/init.cpio > init.gz')

os.system('qemu-system-x86_64 --version')
print('Booting ...\n', flush=True)
cmd = "qemu-system-x86_64 -m 1337M -kernel /home/ctf/bzImage -initrd init.gz -append 'console=ttyS0 nokaslr panic=-1' -nographic -no-reboot"
os.system(cmd)
