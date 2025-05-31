import os
from base64 import b64decode

class CrypTopiaShell():

    # THE VALUES OF P AND K ARE NOT THE CORRECT ONES AND ARE ONLY PLACEHOLDERS
    P = 0xdf5321e0a509b27419d9680b0a20698c841b6420906047d58b15ae331df19f0ac38703bd109e64098e77567ffb62fe2814be54e0e1a3aef9a5e58f5bf7a8437d41a6402aad078ae4d118274337bb0b1e2c943ae7c3f9f12c3602560434e5fc1dc373a272259b6d803731e696e4c9f9ef0420ff95225f321d81c3650a469240c523e81a26134dcbdf0b12ba941c09b0aae856fc4fdd6b8f1cf7a7e61796d042dc3921d7d0231338008ee1fe8f2f9d33ea0d669d9c25af51df10ab3ef612e3071088abef9572aa82228791a7bf218771de5db5ebec68a405f9646e05d44cae5932c5e0a1c95b672fd3d1a2f120b918391391c7cd569e59656904ac7f14cb33e4bb
    K = 0x9f9798d08dc88586a04a234525f591413e8d45b13d1ffe2c071e281d28bd8381

    G = 0x8b6eec60fae5681c
    MAGIC = b"\x01\x02CrypTopiaSig\x03\x04"

    def __sign(self, gen, key, mod):
        bl = gen.bit_length()
        for i in range(len(self.data)):
            gen = (gen ^ (self.data[i] << (i % bl))) & 2**bl-1
        s = 1
        while key:
            if key & 1:
                s = s * gen % mod
            key = key >> 1
            gen = gen * gen % mod
        return s

    def create(self, data):
        self.data = data
        self.signature = self.__sign(self.G, self.K, self.P).to_bytes(self.P.bit_length()//8, 'big')
        self.header = self.MAGIC + len(self.data).to_bytes(6, 'big') + len(self.signature).to_bytes(6, 'big')

    def parse(self, data):
        if data[:len(self.MAGIC)]!= self.MAGIC:
            print("Missing magic bytes")
            return False
        length = int.from_bytes(data[len(self.MAGIC):len(self.MAGIC)+6], 'big')
        signature_length = int.from_bytes(data[len(self.MAGIC)+6:len(self.MAGIC)+12], 'big')
        if len(data) > len(self.MAGIC)+12+length+signature_length:
            print("Invalid data size")
            return False
        self.data = data[len(self.MAGIC)+12:len(self.MAGIC)+12+length]
        self.signature = data[len(self.MAGIC)+12+length:len(self.MAGIC)+12+length+signature_length]
        if self.__sign(self.G, self.K, self.P).to_bytes(self.P.bit_length()//8, 'big') != self.signature:
            print("Invalid signature")
            return False
        return True

    def run(self):
        try:
            os.system(self.data)
        except Exception as e:
            print(f"Woops! Something went wrong")

    def dump(self):
        return self.header + self.data + self.signature

ctc = CrypTopiaShell()

print("Welcome to CrypTopiaShell!\nProvide base64 encoded shell commands in the CrypTopiaSig format in order to get them executed.")

while True:
    try:
        data = input("$ ")
        try:
            data = b64decode(data)
        except:
            print("Invalid base64 data")
            continue
        try:
            if not ctc.parse(data):
                continue
            ctc.run()
        except:
            print(f"Invalid CrypTopiaSig file")
    except:
        break
