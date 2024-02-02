#!/usr/local/bin/python

import pyhelayers
import numpy as np
import base64
import sys
import os
os.chdir("/tmp")

THRESHOLD = 0.25

he_context = pyhelayers.HeaanContext()
he_context.load_from_file("/app/public.key")
he_context.load_secret_key_from_file("/app/private.key")
encoder = pyhelayers.Encoder(he_context)

data = input("Please provide a base64 encoded ciphertext equal to 1/x\n")

cx = encoder.encode_encrypt([0])
cy = encoder.encode_encrypt([0])
cx.load_from_file("/app/x.ctxt")

try:
	cy.load_from_buffer(base64.standard_b64decode(data))
except:
	print("Couldn't load ctxt")
	sys.exit(0)

x = encoder.decrypt_decode_double(cx)
y = encoder.decrypt_decode_double(cy)

if np.max(np.abs(x * y - 1)) < THRESHOLD:
    with open("/app/flag.txt", "r") as f:
        print(f.read())

else:
	print("Error too high")