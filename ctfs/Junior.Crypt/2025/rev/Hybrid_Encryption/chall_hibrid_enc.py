import base64

def encrypt(flag: str) -> str:
    if not flag.startswith("grodno{") or not flag.endswith("}"):
        return "" 
    encoded = bytes([ord(c) ^ 0xAA for c in flag[7:-1]])
    return base64.b64encode(encoded).decode()

def check_flag(flag: str) -> bool:
    return encrypt(flag) == "np2Z3p2c3s6YmZ3ezs2ZmM/Tnc7NmJmdz5yYm96cz8+Ym53Z3w=="

flag = input("Enter flag: ")
print("Correct!" if check_flag(flag) else "Wrong!")