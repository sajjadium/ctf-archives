import base64

def encrypt_input(input_str):
    flag = input_str
    flag = unknown2(flag, 345345345)
    flag = unknown1(flag)
    flag = unknown2(flag, 0)
    flag = unknown(flag, 18)
    return flag

def check_flag(encrypted_input):
    return encrypted_input == "HL13Oe5cEdBUwYlKM0hONdROENJsFNvz"

def unknown(input_str, something):
    result = []
    for c in input_str:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            offset = (ord(c) - base + something) % 26
            if offset < 0:
                offset += 26
            c = chr(base + offset)
        result.append(c)
    return ''.join(result)

def unknown1(xyz):
    return xyz[::-1]

def unknown2(xyz, integer):
    return base64.b64encode(xyz.encode()).decode()

def main():
    user_input = input("Flag: ")
    encrypted_input = encrypt_input(user_input)

    if check_flag(encrypted_input):
        print("Correct flag! Congratulations!")
    else:
        print("Incorrect flag! Please try again.")

if __name__ == "__main__":
    main()
