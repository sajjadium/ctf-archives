#!/usr/local/bin/python

import numpy as np
from Pyfhel import Pyfhel, PyPtxt, PyCtxt

DEBUG = False

dir_name = "data"
HE = Pyfhel()
HE.load_context(dir_name + "/context")
HE.load_public_key(dir_name + "/pub.key")
HE.load_secret_key("sec.key")
x = PyCtxt(pyfhel=HE, fileName=dir_name + "/c.ctxt")

if DEBUG:
    y = PyCtxt(pyfhel=HE, fileName="sol.ctxt")
else:
    ctxt_bytes = input("hex-encoded matrix inverse ciphertext: ")
    ctxt_bytes = bytes.fromhex(ctxt_bytes)
    y = PyCtxt(pyfhel=HE, bytestring=ctxt_bytes)


n = 2**14
slots = n // 2
m = 8
num_mtx = slots // (m*m)

mat = HE.decryptFrac(x).reshape((num_mtx,m,m))
imat = HE.decryptFrac(y).reshape((num_mtx,m,m))

max_err = 0.0
Id = np.identity(m)
for i in range(num_mtx):
    M = mat[i]
    Mi = imat[i]
    v = M @ Mi
    err = np.max(np.abs(v - Id))
    if err > max_err:
        max_err = err
    if not np.isfinite(err):
        max_err = 1e10

if max_err < 0.025:
    print("Success!")

    with open("flag.txt", "r") as f:
        flag = f.read()
        print(flag)

else:
    print("Too much error!")
