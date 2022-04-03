from flag import FLAG

F = GF(2^9)
n, k = 256, 128

RS = [codes.GeneralizedReedSolomonCode(sample(F.list(), n), k) for _ in range(2)]
G = block_matrix([
    [RS[0].generator_matrix(), random_matrix(F, k, n)],
    [zero_matrix(F, k, n), RS[1].generator_matrix()]])
S = matrix(GL(2*k, 2).random_element())
P = matrix(F, Permutations(2*n).random_element().to_matrix())

Gp =  S * G * P
d = (RS[0].minimum_distance() - 1) // 2
FLAG += os.urandom(2*k - len(FLAG))
m = vector(F.fetch_int(x) for x in FLAG)

e = []
for _ in range(2):
    _e = [F.random_element() for i in range(d)] + [F(0)]*(n-d)
    shuffle(_e)
    e.extend(_e)

c = m*Gp + vector(e)

save(Gp, "pubkey.sobj")
save(c, "encrypted.sobj")
