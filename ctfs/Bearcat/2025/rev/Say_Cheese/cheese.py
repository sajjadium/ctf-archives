import base64

def encoder(input_str, key):
    encoded_chars = []
    for i in range(len(input_str)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(input_str[i]) + ord(key_c)) % 256)
        encoded_chars.append(encoded_c)
    encoded_str = ''.join(encoded_chars)
    return base64.b64encode(encoded_str.encode()).decode()

def main():
    print("""         _--"-.
      .-"      "-.
     |""--..      '-.
     |      ""--..   '-.
     |.-. .-".    ""--..".
     |'./  -_'  .-.      |
     |      .-. '.-'   .-'
     '--..  '.'    .-  -.
          ""--..   '_'   :
                ""--..   |
                      ""-' """)
    ciphertext = "wpbCi8KIwpfCh8OPwph5wqnCosK6woTCqcKnwq13wrfCh8KzwqnCpMKKccOJwrh8wqTCl3LDgcKHw4U="
    key = "THECAT"
    inp = input("Enter your cat: ")
    encoded_flag = encoder(inp, key)
    if ciphertext == encoded_flag:
        print("YAY you found the cat!")
    else:
        print("Not so easy cheesy huh?")

if __name__ == "__main__":
    main()

