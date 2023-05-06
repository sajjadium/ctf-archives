import os
import mmap


DEFAULT_FLAG = 'tstlss{XXXXXXXXXXXXXXXXXXXXXXXXXXXXX}'
DEFAULT_IP = '133.133.133.133'

ip = os.getenv('IP')
flag = os.getenv('FLAG')


if ip is None:
    print("Please specify an ip via the IP environment variable.")
    exit(-1)

if len(ip) > len(DEFAULT_IP):
    print("Please specify an ip with less characters")
    exit(-1)

if flag is not None and len(flag) > len(DEFAULT_FLAG):
    print("Please specify a flag with less characters")
    exit(-1)

with open('/images/root.dsk', 'rw+b') as f:
    mapped_file = mmap.mmap(f.fileno(), 0)

    mapped_file.seek(mapped_file.find(DEFAULT_IP))
    mapped_file.write(ip.ljust(len(DEFAULT_IP), '\x00'))
    if flag is not None:
        mapped_file.seek(mapped_file.find(DEFAULT_FLAG))
        mapped_file.write(flag.ljust(len(DEFAULT_FLAG), '\x00'))
