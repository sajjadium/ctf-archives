import jamal_secrets
from Crypto.Random.random import randrange
from Crypto.Util.number import bytes_to_long, inverse, long_to_bytes

p = 23913162461506241913954601592637284046163153526897774745274721709391995411082414294401609291264387860355671317653627011946189434760951108211821677155027175527596657912855025319457656605884632294211661524895665376213283136003484198594304828143112655895399585295073436422517502327322352675617692540534545273072811490753897471536886588395908046162672249608111996239705154693112925449400691756514248425452588443058856375927654703767484584645385639739363661773243428539784987039554945923457524757103957080876709268568549852468939830286998008334302308043256863193950115079756866029069932812978097722854877041042275420770789
g = 2


def generate_key():
    x = randrange(p // 2, p - 1)
    h = pow(g, x, p)
    return x, h


def encrypt(msg, h):
    y = randrange(1, p - 1)
    s = pow(h, y, p)
    r = pow(g, y, p)
    c = bytes_to_long(msg) * s % p
    return r, c


def decrypt(ct, x):
    r, c = ct
    s = pow(r, x, p)
    inv_s = inverse(s, p)
    return long_to_bytes(c * inv_s % p)


def main():
    x, h = generate_key()
    assert b'test' == decrypt(encrypt(b'test', h), x)
    print('h=%d' % h)

    f1, r1, c1 = jamal_secrets.part1(h)
    assert f1 == decrypt((r1, c1), x)
    assert r1 == 1
    print('c1=%d' % c1)

    (f2, r2, c2), (f3, r3, c3) = jamal_secrets.part2(h)
    assert f2 == decrypt((r2, c2), x)
    assert f3 == decrypt((r3, c3), x)
    assert r2 == r3
    assert f1 == f2
    print('c2=%d' % c2)
    print('c3=%d' % c3)

    (f4, r4, c4), (f5, r5, c5) = jamal_secrets.part3(h)
    assert f4 == decrypt((r4, c4), x)
    assert f5 == decrypt((r5, c5), x)
    assert r5 == pow(r4, 2, p)
    assert f3 == f4
    print('c4=%d' % c4)
    print('c5=%d' % c5)

    (f6, r6, c6), (f7, r7, c7) = jamal_secrets.part4(h)
    assert f6 == decrypt((r6, c6), x)
    assert f7 == decrypt((r7, c7), x)
    assert r7 == g * r6 % p
    assert f5 == f6
    print('c6=%d' % c6)
    print('c7=%d' % c7)

    # print("Flag is", (f1 + f3 + f5 + f7).strip())


main()
