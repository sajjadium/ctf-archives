from Crypto.Util.number import getPrime, inverse, bytes_to_long
def flash_key():
    while True:
        p = getPrime(1024)
        q = getPrime(1024)
        N = p * q
        #you can't even use weiner's attack now hahaha
        dp_smart= getPrime(16)
        try:
            e = inverse(dp_smart, p-1)
            return N, e, dp_smart
        except ValueError:
            continue

N, e, _= flash_key()

flag = b"flag{REDACTED}"
m = bytes_to_long(flag)
c = pow(m, e, N)
print("Need for Speed")
print("Since Wiener said calculating d_p and d_q is fast, I decided to make it even faster 'cause I am smarter.")
print(f"N = {N}")
print(f"e = {e}")
print(f"c = {c}")