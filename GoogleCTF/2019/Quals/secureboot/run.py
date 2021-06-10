#!/usr/bin/python3
import os
import tempfile

fname = tempfile.NamedTemporaryFile().name

os.system("cp OVMF.fd %s" % (fname))
os.system("chmod u+w %s" % (fname))
os.system("qemu-system-x86_64 -monitor /dev/null -m 128M -drive if=pflash,format=raw,file=%s -drive file=fat:rw:contents,format=raw -net none -nographic 2> /dev/null" % (fname))
os.system("rm -rf %s" % (fname))
