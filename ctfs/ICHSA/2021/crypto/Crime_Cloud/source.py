import base64
import os
import zlib


def rand(n):
    return os.urandom(n)

def xor(a,b):
    return bytes(x^y for x,y in zip(a,b))

def enc_otp(pt):
    return xor(pt, rand(len(pt)))

def process(req):
    pt = zlib.compress(b"ICHSA_CTF{fake_flag_to_annoy_you_pay_us_ten_thousand_BTC}" + rand(32) + req)
    return enc_otp(pt)


def main():
    print("Wellcome!\nInput an empty line to exit.")
    while True:
        req = input("\nYour input: ")
        if len(req) == 0:
            print("Bye!")
            break
        req_bytes = req.encode()
        if len(req_bytes) > 128:
            print(f'Bad input length {len(req_bytes)} > 128')
            continue
        print(base64.b64encode(process(req_bytes)).decode())

if __name__ == "__main__":
   try:
      main()
   except:
      print("Some error occured")
