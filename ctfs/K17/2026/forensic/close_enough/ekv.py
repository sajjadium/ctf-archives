class EncryptedKV:
    def __init__(self, secret):
        self.secret = secret
        self.d = {}

    def __getitem__(self, key):
        num: int = (self.d[key] ^ self.secret)
        return num.to_bytes(-(num.bit_length() // -8)).decode()
    
    def __setitem__(self, key, value):
        self.d[key] = int.from_bytes(value.encode()) ^ self.secret
