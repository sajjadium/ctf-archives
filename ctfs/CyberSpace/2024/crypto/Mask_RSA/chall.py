from Crypto.Util.number import getPrime, bytes_to_long

FLAG = open('flag.txt', 'rb').read().strip()

def mask_expr(expr):
    global e, n
    assert '**' not in expr, "My computer is weak, I can't handle this insane calculation"
    assert len(expr) <= 4, "Too long!"
    assert all([c in r'pq+-*/%' for c in expr]), "Don't try to break me"
    res = eval(expr)
    return str(pow(res, e, n))[::2]

if __name__ == '__main__':

    e = 3
    p, q = 1, 1
    while p == q:
        while (p-1) % e == 0:
            p = getPrime(513)
        while (q-1) % e == 0:
            q = getPrime(513)

    m = bytes_to_long(FLAG)
    n = p * q
    c = pow(m, e, n)
    print(f'{c = }')
    for _ in range(20):
        expr = input('Input your expression in terms of p, q and r: ')
        print(mask_expr(expr))
