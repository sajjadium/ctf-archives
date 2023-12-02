from Crypto.Cipher import AES
import struct
import math

class InvalidTagError(Exception):
    def __init__(self, message="Invalid Authentication Tag"):
        self.message = message
        super().__init__(self.message)

class MAC:
    MASK_R = 0x1337fffc0ffffffc0ffffffc0fff1337
    MASK_S = 0xffffffffffffffffffffffffffffffff
    P      = 0x7ffffffffffffffffffffffffffffffbb
    Q      = 0x100000000000000000000000000000000

    def __init__(self, key: bytes) -> None:
        if len(key) != 0x20:
            raise ValueError("[MAC Error]: The key's length must be (in byte)")

        self.r = int.from_bytes(key[0x00:0x10], byteorder='little') & self.MASK_R
        self.s = int.from_bytes(key[0x10:0x20], byteorder='little') ^ self.MASK_S

    def commit(self, message):
        res = 0
        
        for i in range(0, math.ceil(len(message)/0x10)):
            res += int.from_bytes(message[i*0x10:(i+1)*0x10], byteorder='little') + self.Q
            res  = (self.r * res) % self.P
            
        res = (res + self.s) % self.Q
        return int.to_bytes(res, length=0x10, byteorder='little')

class AEMC:
    @classmethod
    def pad(self, data, size):
        if len(data) % size == 0:
            return data
        else:
            return data + bytes(size - len(data)%size)
        
    @classmethod
    def verify_auth_tag(self, tag_a, tag_b):
        if len(tag_a) != len(tag_b):
            return False

        ok = 0
        for x, y in zip(tag_a, tag_b):
            ok |= x ^ y

        return ok == 0

    @classmethod
    def generate_mac_key(self, master_key, nonce):
        cipher = AES.new(key=master_key, mode=AES.MODE_CTR, nonce=nonce)
        return cipher.encrypt(bytes(0x20))

    def __init__(self, master_key) -> None:
        if len(master_key) != 0x20:
            raise ValueError("Master key must be 256 bits long")

        self.master_key = master_key

    def encrypt(self, plaintext, nonce, associated_data=None):
        return self.__encrypt(
            plaintext=plaintext,
            nonce=nonce,
            associated_data=associated_data if associated_data is not None else b""
        )

    def decrypt(self, ciphertext, nonce, associated_data=None):
        return self.__decrypt(
            ciphertext_tag=ciphertext,
            nonce=nonce,
            associated_data=associated_data if associated_data is not None else b""
        )

    def __encrypt(self, plaintext, associated_data, nonce):
        if len(nonce) != 12:
            raise ValueError("Nonce must be 96 bits long")
        
        mac_key    = self.generate_mac_key(self.master_key, nonce)
        ciphertext = AES.new(
            key=self.master_key, mode=AES.MODE_CTR, nonce=nonce
        ).encrypt(plaintext=plaintext)

        mac_data   = self.pad(associated_data, 0x10)
        mac_data  += self.pad(ciphertext, 0x10)
        mac_data  += struct.pack('<QQ', len(associated_data), len(ciphertext))
        auth_tag   = MAC(key=mac_key).commit(message=mac_data)
        
        return ciphertext + auth_tag
    
    def __decrypt(self, ciphertext_tag, associated_data, nonce):
        if len(nonce) != 12:
            raise ValueError("Nonce must be 96 bits long")
        
        ciphertext   = ciphertext_tag[:-0x10]
        expected_tag = ciphertext_tag[-0x10:]
        mac_key      = self.generate_mac_key(self.master_key, nonce)

        # verify auth_tag
        mac_data       = self.pad(associated_data, 0x10)
        mac_data      += self.pad(ciphertext, 0x10)
        mac_data      += struct.pack('<QQ', len(associated_data), len(ciphertext))
        calculated_tag = MAC(key=mac_key).commit(message=mac_data)

        if not self.verify_auth_tag(expected_tag, calculated_tag):
            raise InvalidTagError("No Hack!")
        
        return AES.new(
            key=self.master_key, mode=AES.MODE_CTR, nonce=nonce
        ).decrypt(ciphertext=ciphertext)