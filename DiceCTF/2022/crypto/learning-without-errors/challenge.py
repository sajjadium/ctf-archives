# https://github.com/sarojaerabelli/py-fhe
import sys
sys.path.append("./py-fhe")

from ckks.ckks_decryptor import CKKSDecryptor
from ckks.ckks_encoder import CKKSEncoder
from ckks.ckks_encryptor import CKKSEncryptor
from ckks.ckks_evaluator import CKKSEvaluator
from ckks.ckks_key_generator import CKKSKeyGenerator
from ckks.ckks_parameters import CKKSParameters

import json

class Challenge:
    def __init__(self, poly_degree, ciph_modulus):
        big_modulus = ciph_modulus**2
        scaling_factor = 1 << 30
        
        params = CKKSParameters(poly_degree=poly_degree,
                                ciph_modulus=ciph_modulus,
                                big_modulus=big_modulus,
                                scaling_factor=scaling_factor)
        key_generator = CKKSKeyGenerator(params)
        public_key = key_generator.public_key
        secret_key = key_generator.secret_key
        encoder = CKKSEncoder(params)
        encryptor = CKKSEncryptor(params, public_key, secret_key)
        decryptor = CKKSDecryptor(params, secret_key)
        evaluator = CKKSEvaluator(params)
        
        self.poly_degree = poly_degree
        self.ciph_modulus = ciph_modulus
        self.scaling_factor = scaling_factor
        
        self.secret_key = secret_key
        
        self.encoder = encoder
        self.encryptor = encryptor
        self.decryptor = decryptor
        self.evaluator = evaluator

    def encrypt_flag(self):
        with open("flag.txt", "rb") as f:
            flag = f.read()
        
        n = self.poly_degree//2
        
        flag = int.from_bytes(flag, "big")
        flag = f"{flag:0{n}b}"
        flag = [float(i) for i in flag]
        
        d = {"real_part": flag,
             "imag_part": [0]*n}
        ciph = self.encrypt_json(d)
        return ciph
    
    def dump_ciphertext(self, ciph):
        d = {"c0" : ciph.c0.coeffs,
             "c1" : ciph.c1.coeffs,
             "poly_degree" : ciph.c0.ring_degree,
             "modulus" : ciph.modulus}
        return d

    def dump_plaintext(self, plain):
        d = {"m" : plain.poly.coeffs,
             "poly_degree" : plain.poly.ring_degree,
             "scaling_factor" : plain.scaling_factor}
        return d
    
    def dump_decoded_plaintext(self, plain):
        x = [complex(i) for i in plain]
        real = [i.real for i in plain]
        imag = [i.imag for i in plain]
        d = {"real_part": real,
             "imag_part": imag}
        return d

    def decrypt_ciphertext(self, ciph):
        plain = self.decryptor.decrypt(ciph)
        return plain

    def decrypt_and_decode_ciphertext(self, ciph):
        plain = self.decryptor.decrypt(ciph)
        plain = self.encoder.decode(plain)
        return plain

    def encrypt_json(self, d):
        real = list(d["real_part"])
        imag = list(d["imag_part"])
        
        message = [r + 1j * i for r,i in zip(real, imag)]
        assert len(message) == self.poly_degree // 2
        
        plain = self.encoder.encode(message, self.scaling_factor)
        ciph = self.encryptor.encrypt(plain)
        return ciph
    
