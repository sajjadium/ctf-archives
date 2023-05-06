from Crypto.Cipher import AES


def nsplit(s: list, n: int):
    return [s[k: k + n] for k in range(0, len(s), n)]


def aes(data: int, key: bytes) -> int:
    data = data.to_bytes(16, 'big')
    E = AES.new(key, AES.MODE_ECB)
    return int.from_bytes(E.encrypt(data), 'big')
