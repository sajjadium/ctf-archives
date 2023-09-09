from binascii import unhexlify
from gzip import decompress
from struct import pack
from datetime import datetime
from zipfile import ZipFile
from io import BytesIO
from pwn import xor

print('start here')