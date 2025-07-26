def gaga(text, key):
    result = []
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return result

key = "IWANTMOMOS"

encrypted= [':', '?', ' ', '%', ' ', '$', ',', '9', ')', '(', '+', 'c', '#', '7', '\x06', '~', '9', '\x12', '~', ' ', '\x16', '4', '4', ':', 'g', '0']
inp= input("> ")

if (gaga(inp, key)==encrypted):
    print("YOU DID ITTT :))")
else:
    print("try again :(")