#!/usr/bin/python -u
import os
import time
from backports import tempfile
time.sleep(1)
dirname = os.path.abspath(os.path.dirname(__file__))
pemu = os.path.join(dirname, "pemu", "loader")
bin = os.path.join(dirname, "binary", "main")
with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    os.system("%s %s" % (pemu, bin))

