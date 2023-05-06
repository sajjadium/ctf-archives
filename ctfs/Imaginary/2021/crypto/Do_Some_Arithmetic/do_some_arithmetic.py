from Crypto.Util.number import bytes_to_long
import hashlib, random

with open("flag.txt", "rb") as f:
    flag = bytes_to_long(f.read().strip())

rnd = random.SystemRandom()

def H(m):
    return bytes_to_long(hashlib.sha256(m).digest())

def sign(m, x):
    k = pow(g2, rnd.randint(1, q - 1), q)
    r = pow(g, k, p) % q
    s = (pow(k, -1, q) * (H(m) + x*r)) % q
    return r, s

def verify(m, r, s, y):
    if not (0 < r < q) and (0 < s < q): return False
    w = pow(s, -1, q)
    u1 = (H(m) * w) % q
    u2 = (r * w) % q
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
    return v == r

q = 0xe53da909dc6d024303968079585b10104f1954c5f19a0a2f1f916825307584ef
p = 0x72889571adfe39826bbc112eb2141618765c956780a035e9e2c4dd8cf190008aa92044c5eefa89bc97ed04f4b9b3f26c3692e8c5ef459aa82011c67e90fb1ddff1c413b235139c1b6f0b49548bf69872f8151482a5e88ff1903f0941f7ad9526a6b11648813528759b0425575a8ee9f4b6593ab1b508c21b70f430e91606c2b43718f9474f84039e14db85698bfd4994525efa8307bec42d4eecf9e253981bc58ab971c83542cd34f309d06aa14697e10368be0f72a1594584e8381db5c38c654e93257f59f0b03c3fa1a247a559e7aa94af229ec307795b579933c69b1717d3f665837cd685897a3e2ae3ebb230787233edfc08b3012c91347637c14f2938e3
g = 0x3c990a52040518d9800802965a8404164a9ef5e4d6dcbf65444cc4a610fdaee929dc5fcc98279f7ba8246ef310ef5cd578fed68a5289c63dd849685eb10636cab5cf4e6e1af3229d87331524a6018706f8c13a9464746b854c814109807d7fcc24186b3b24725aaa595829b4af4777e5ad4dc532474772e4b4dc7f81df10faf545d4af766d4dc9555a969779e1c51f5474c7406535860001085f20bab6cf8647737c575bf794ad21e68b215ad1c7cea74d49fd3f0ed4500d97b314b7b1a09687660552f079304bf1994122eb616d8d132e6518983a59ec9a3c1d9b4512019fcef74818ee632200a1f4264c2078176129e0326d700817208385c11d2a5fd31ecc
g2 = 0x7859f6fd681b89043c6d67194def5f95415ac01863887405df6819bffe6edf6f


assert flag < q
y = pow(g, flag, p)

m = b"Signing things, just for fun"
r, s = sign(m, flag)
assert verify(m, r, s, y)

with open("output.txt", "w") as f:
    f.write(f"{y = }\n")
    f.write(f"{r = }\n")
    f.write(f"{s = }\n")
