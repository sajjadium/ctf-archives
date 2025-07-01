import time

def dynamic_key():
    return ((int(time.time()) % 256) ^ 0xFF) & 0x7F

def encrypt(s, key):
    return bytes([(c + key) ^ (i * 2) for i, c in enumerate(s.encode())])

def check_flag(flag: str) -> bool:
    if not flag.startswith("grodno{") or not flag.endswith("}"):
        return False
    
    middle = flag[7:-1]
    
    key = dynamic_key()
    encrypted = encrypt(middle, key)
    expected = b'\x74\xab\x9a\x62\x95\x6b\x9f\x81\x6b\x87\xbd\x99\x81\xb9\x93\x98\xb5\x80\x8d\xa9\x5b\x4a\xb1\x8e\xac\xa7\x9c\xb9\xa9\xa4\xa8\xb1\x39\xdc\xd7\x26\xd5\xea\xee\xdb\xc8\xc7\xca\xf5\x39\xc8\xc0\xcb'
    
    return encrypted == expected

flag = input("Enter flag: ")
print("Correct!" if check_flag(flag) else "Wrong!")