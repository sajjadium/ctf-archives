import numpy as np

from Crypto.Hash import SHAKE256
from Crypto.Util.strxor import strxor

def encrypt(s, flag):
	raw = bytes(np.mod(s, 256).tolist())
	shake = SHAKE256.new()
	shake.update(raw)
	pad = shake.read(len(flag))
	return strxor(flag, pad)