p = 55899879511190230528616866117179357211
V = GF(p)^3
R.<x> = PolynomialRing(GF(p))
f = x^3 + 36174005300402816514311230770140802253*x^2 + 35632245244482815363927956306821829684*x + 10704085182912790916669912997954900147
Q = R.quotient(f)

def V_pow(A, n):
    return V([a^n for a in list(A)])

n, m = randint(1, p), randint(1, p)
A = Q.random_element()
B = Q.random_element()
C = A^n * B^m

print(' '.join(map(str, list(A))))
print(' '.join(map(str, list(B))))
print(' '.join(map(str, list(C))))

phi_A = V(list(map(int, input().split())))
phi_B = V(list(map(int, input().split())))
phi_C = V(list(map(int, input().split())))

check_phi_C = V_pow(phi_A, n).pairwise_product(V_pow(phi_B, m))

if phi_C == check_phi_C:
    print(open('./flag.txt', 'r').read().strip())
