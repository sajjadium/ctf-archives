def check_flag(flag):
    enc = [0x6e, 0x49, 0x60, 0x9, 0x78, 0x75, 0x1, 0x3f, 0x58, 0x68, 0x4f]
    key = b"MYSECRETKEY"
    if not flag.startswith("grodno{") or not flag.endswith("}") or len(flag) != 30:
        return False
    
    middle = flag[7:-1]
    for i in range(11):
        if (ord(middle[i*2]) ^ ord(middle[i*2+1])) != enc[i] ^ key[i]:
            return False
    return True

flag = input("Enter flag: ")
if check_flag(flag):
    print("Correct!")
else:
    print("Wrong!")