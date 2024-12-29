from hashlib import md5
import random

secure_random = random.SystemRandom()
ls = list(prime_range(3,117))
p = 4 * prod(ls) - 1
F = GF(p)
E = EllipticCurve(F, [1, 0])

output = ""

for i in range(500):
    w = secure_random.choice(ls)
    while (P := E.random_point() * ((p + 1) // w)) == E(0):
        pass
    phi = E.isogeny(P)
    for j in range(3):
        Q = E.random_point(); R = phi(Q)
        output += f"{Q[0]}, {R[0]}\n"
    E = phi.codomain()
    
FLAG = "wgmy{" + md5(str(E.j_invariant()).encode()).hexdigest() + "}"
print(FLAG)
f = open("output.txt", "w")
f.write(output)