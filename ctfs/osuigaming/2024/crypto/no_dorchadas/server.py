from hashlib import md5
from secret import flag, secret_slider
from base64 import b64encode, b64decode

assert len(secret_slider) == 244
dorchadas_slider = b"0,328,33297,6,0,B|48:323|61:274|61:274|45:207|45:207|63:169|103:169|103:169|249:199|249:199|215:214|205:254,1,450.000017166138,6|6,1:1|2:1,0:0:0:0:"

def sign(beatmap):
    hsh = md5(secret_slider + beatmap)
    return hsh.hexdigest()

def verify(beatmap, signature):
    return md5(secret_slider + beatmap).hexdigest() == signature

def has_dorchadas(beatmap):
    return dorchadas_slider in beatmap

MENU = """
--------------------------
| [1] Sign a beatmap     |
| [2] Verify a beatmap   |
--------------------------"""

def main():
    print("Welcome to the osu! Beatmap Signer")
    while True:
        print(MENU)
        try:
            option = input("Enter your option: ")
            if option == "1":
                beatmap = b64decode(input("Enter your beatmap in base64: "))
                if has_dorchadas(beatmap):
                    print("I won't sign anything with a dorchadas slider in it >:(")
                else:
                    signature = sign(beatmap)
                    print("Okay, I've signed that for you: " + signature)
            elif option == "2":
                beatmap = b64decode(input("Enter your beatmap in base64: "))
                signature = input("Enter your signature for that beatmap: ")
                if verify(beatmap, signature) and has_dorchadas(beatmap):
                    print("How did you add that dorchadas slider?? Anyway, here's a flag: " + flag)
                elif verify(beatmap, signature):
                    print("Signature is valid!")
                else:
                    print("Signature is invalid :(")
        except:
            print("An error occurred!")
            exit(-1)

main()