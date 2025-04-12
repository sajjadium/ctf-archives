from random import randint

def generate_OTP():
    OTP = b''
    for _ in range(10):
        OTP += int.to_bytes(randint(0,255))
    return OTP

def encrypt_file(input_file: str, output_file: str, passwd: bytes):
    with open(input_file, "rb") as ifile:
        input_data = ifile.read()

    with open(output_file, 'wb') as ofile:
        buffer = bytes([(input_data[k] ^ passwd[k % len(passwd)]) for k in range(len(input_data))])
        ofile.write(buffer)

if __name__ == '__main__':
    otp = generate_OTP()
    input_file = input("Entrer le nom du fichier à chiffrer: ").lower()
    output_file = input_file + '.encrypted'
    encrypt_file(input_file, output_file, otp)
    print(f"Le fichier {input_file} a été chiffré avec succès.")




    
