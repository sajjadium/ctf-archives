import sys

def validate_flag(flag):
    encoded_flag = encode_flag(flag)
    expected_flag = 'ZT_YE\\0|akaY.LaLx0,aQR{"C'
    if encoded_flag == expected_flag:
        return True
    else:
        return False

def encode_flag(flag):
    encoded_flag = ""
    for c in flag:
        encoded_char = chr((ord(c) ^ 0xFF) % 95 + 32)
        encoded_flag += encoded_char
    return encoded_flag

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <flag>")
        sys.exit(1)
    input_flag = sys.argv[1]
    if validate_flag(input_flag):
        print("Correct flag!")
    else:
        print("Incorrect flag.")

if __name__ == "__main__":
    main()