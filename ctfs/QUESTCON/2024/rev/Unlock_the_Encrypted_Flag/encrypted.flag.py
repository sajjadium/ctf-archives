### THIS FUNCTION WILL NOT HELP YOU FIND THE FLAG --LT ########################
def str_xor(secret, key):
    new_key = key
    i = 0
    while len(new_key) < len(secret):
        new_key = new_key + key[i]
        i = (i + 1) % len(key)        
    return "".join([chr(ord(secret_c) ^ ord(new_key_c)) for (secret_c, new_key_c) in zip(secret, new_key)])
###############################################################################

flag_enc = open('flag.txt.enc', 'rb').read()

def level_1_pw_check():
    user_pw = input("Please enter correct password for flag: ")
    
    pw_parts = ["ak98", "-=90", "adfjhgj321", "sleuth9000"]
    obfuscated_pw = "".join(pw_parts)  

    if (user_pw.startswith("ak") and user_pw.endswith("9000")) and \
       (len(user_pw) == len(obfuscated_pw)):
        print("Welcome back... your flag, user:")
        decryption = str_xor(flag_enc.decode(), "utilitarian")
        print(decryption)
        return
    print("That password is incorrect")

level_1_pw_check()
