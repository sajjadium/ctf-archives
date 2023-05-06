from Crypto.Util.number import getPrime,inverse,long_to_bytes,bytes_to_long
from Crypto.PublicKey import RSA
flag = "shellctf{something_here}"

n = getPrime(4096)
e = 65537
phi = (n-1)*(n-1)
d = inverse(e,phi)

encrypted_flag = pow(bytes_to_long(flag.encode()),e,n)

decrypted_flag = long_to_bytes(pow(encrypted_flag,d,n)).decode()

assert decrypted_flag == flag 
print(RSA.construct((n,e)).publickey().exportKey().decode())
print("c = ",encrypted_flag)
