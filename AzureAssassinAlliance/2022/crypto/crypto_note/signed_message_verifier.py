from gmssl import sm2, sm3, func # gmssl==3.2.1
from binascii import a2b_hex
from json import load
from secret import bob_pub

class SM2(sm2.CryptSM2):
    def __init__(self, private_key, public_key):
        ecc_table = {
            'n': '1000000000000000000000000000000014DEF9DEA2F79CD65812631A5CF5D3ED',
            'p': '7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFED',
            'g': '2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD245A'\
                '20AE19A1B8A086B4E01EDD2C7748D14C923D4D7E6D7C61B229E9C5A27ECED3D9',
            'a': '2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA984914A144',
            'b': '7B425ED097B425ED097B425ED097B425ED097B425ED097B4260B5E9C7710C864',
        }
        super().__init__(private_key, public_key, ecc_table)

    def _sm3_z(self, data):
        z = '0080'+'31323334353637383132333435363738' + \
            self.ecc_table['a'] + self.ecc_table['b'] + self.ecc_table['g']
        z = a2b_hex(z)
        Za = sm3.sm3_hash(func.bytes_to_list(z))
        M_ = (Za + data.hex()).encode()
        e = sm3.sm3_hash(func.bytes_to_list(a2b_hex(M_)))
        return e

    def sign_with_sm3(self, data, random_hex_str=None):
        sign_data = a2b_hex(self._sm3_z(data).encode())
        if random_hex_str is None:
            random_hex_str = func.random_hex(self.para_len)
        sign = self.sign(sign_data, random_hex_str)
        return sign

    def verify_with_sm3(self, sign, data):
        sign_data = a2b_hex(self._sm3_z(data).encode())
        return self.verify(sign, sign_data)

def get_bob_sign_pub():
    x, y = bob_pub
    p = 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFED
    delta = 0X2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD2451
    x, y = (x + delta) % p, y
    return hex(x)[2:].zfill(64)+hex(y)[2:].zfill(64)

if __name__ == '__main__':
    text, sign = load(open('signed_message_from_bob.json'))
    verifier = SM2(public_key=get_bob_sign_pub(), private_key=None)
    print('verified' if verifier.verify_with_sm3(sign, text.encode()) else 'tampered')