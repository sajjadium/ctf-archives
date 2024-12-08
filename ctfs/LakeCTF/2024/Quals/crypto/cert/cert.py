from binascii import hexlify, unhexlify
from Crypto.Util.number import bytes_to_long, long_to_bytes
from precomputed import message, signature, N, e
from flag import flag


if __name__ == "__main__":
    print(message + hexlify(long_to_bytes(signature)).decode())
    cert = input(" > ")
    try: 
        s = bytes_to_long(unhexlify(cert))
        assert(s < N)
        if pow(s,e,N)==bytes_to_long("admin".encode()):
            print(flag)
        else:
            print("Not admin")
    except:
        print("Not admin")



        

