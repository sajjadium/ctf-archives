import os
from ECDSA import create_sig, check_sig, generate_private_key, generate_public_key


KEYFILE = "secret_key"


def load_keys():
    if not os.path.isfile(KEYFILE):
        privkey = generate_private_key()
        open(KEYFILE, "w").write(str(privkey))
    else:
        privkey = int(open(KEYFILE, "r").read())
    
    pubkey = generate_public_key(privkey)

    return privkey, pubkey


def main():
    print("Signed code execution unit.")
    print("This system is secured using the CSR2023 curve.")
    print("Allowed signed code example: ls,14408182934124218151903307811921310001651299367247060850011183541272843542567,23712285447829893866902811903350640943324417901907006510465722299556044144317")
    print("To get your code signed, contact your local administrat0r!")
    
    _, pubkey = load_keys()

    user_input = input("Signed shell program:")

    program, r, s = user_input.split(",")
    signature = int(r), int(s)

    # Only allow signed shell commands
    if check_sig(pubkey, program.encode(), signature):
        os.system(program)
    else:
        print("Invalid signature!")


if __name__ == '__main__':
    main()
