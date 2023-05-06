from secret import FLAG

# Implementation of Edwards Curve41417
# x ** 2 + y ** 2 = 1 + 3617 * x ** 2 * y ** 2
# Formulas from http://hyperelliptic.org/EFD/g1p/auto-edwards.html

P = 2 ** 414 - 17
d = 3617 

def on_curve(p):
    x, y = p
    return (x * x + y * y) % P == (1 + d * x * x * y * y) % P

def inv(x):
    return pow(x, -1, P)

def add(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    x = (x1 * y2 + y1 * x2) * inv(1 + d * x1 * x2 * y1 * y2)
    y = (y1 * y2 - x1 * x2) * inv(1 - d * x1 * x2 * y1 * y2)
    return (x % P, y % P)


def mul(x: int, base):
    ans = (0,1)
    cur = base
    while x > 0:
        if x & 1:
            ans = add(cur, ans)
        x >>= 1
        cur = add(cur, cur)
    return ans

base = (17319886477121189177719202498822615443556957307604340815256226171904769976866975908866528699294134494857887698432266169206165, 34)
assert(on_curve(base))

order = 2 ** 411 - 33364140863755142520810177694098385178984727200411208589594759

msg = int.from_bytes(FLAG, 'big')
assert(msg < 2 ** 410)

enc = mul(pow(msg, -1, order), base)

print(f"{enc = }")

# Have a hint!
bm = (1 << 412) - 1
bm ^= ((1 << 22) -1) << 313
bm ^= ((1 << 22) -1) << 13
bm ^= 1 << 196
hint = bm & pow(msg, -1, order)
print(f"{hint = }")

'''
enc = (29389900956614406804195679733048238721927197300216785144586024378999988819550861039522005309555174206184334563744077143526515, 35393890305755889860162885313105764163711685229222879079392595581125504924571957049674311023316022028491019878405896203357959)
hint = 323811241263249292936728039512527915123919581362694022248295847200852329370976362254362732891461683020125008591836401372097
'''
