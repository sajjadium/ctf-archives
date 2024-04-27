from sage.all import *

from Crypto.Util.number import bytes_to_long
from secret import flag
import hashlib

flag_start = b'd3ctf{'
assert flag.startswith(flag_start)
flag = flag[len(flag_start):-1]
assert len(flag) == 32

a = 38
b = 25
p = 2**a * 3**b - 1

assert is_prime(p)
Fp = GF(p)

Fpx = PolynomialRing(Fp, "x")
x = Fpx.gen()
Fp2 = Fp.extension(x**2 + 1, "ii")
ii = Fp2.gen()

A0 = Fp2(6)
E0 = EllipticCurve(Fp2, [0, A0, 0, 1, 0])
E0.set_order((p+1)**2)


sqrtof2 = Fp2(2).sqrt()
f = x**3 + A0 * x**2 + x

Pa = E0(0)
Qa = E0(0)
Pa_done = False
Qa_done = False
d = 0
for c in range(0, p):
    Rx = ii + c
    Ry_square = f(ii + c)
    if not Ry_square.is_square():
        continue
    Ra = E0.lift_x(Rx)
    Pa = 3**b * Ra

    Ta = 2 ** (a - 1) * Pa
    if Ta.is_zero():
        continue
    Tax_plus_3 = Ta.xy()[0] + 3
    if Tax_plus_3 == 2 * sqrtof2 or Tax_plus_3 == -2 * sqrtof2:
        Pa_done = True
    elif Tax_plus_3 == 3 and not Qa_done:
        Qa = Pa
        Qa_done = True
    else:
        raise ValueError('Unexcepted order 2 point.')

    if Pa_done and Qa_done:
        break

assert Pa.order() == 2**a and Qa.order() == 2**a
assert Pa.weil_pairing(Qa, 2**a) ** (2 ** (a - 1)) != 1



Pb = E0(0)
while (3**(b-1))*Pb == 0:
    Pb = 2**a * E0.random_point()
Qb = Pb
while Pb.weil_pairing(Qb, 3**b)**(3**(b-1)) == 1:
    Qb = 2**a * E0.random_point()

print(f'Pa = {Pa.xy()}')
print(f'Qa = {Qa.xy()}')
print(f'Pb = {Pb.xy()}')
print(f'Qb = {Qb.xy()}')


sa = randint(0, 2**a-1)
Ra = Pa + sa * Qa
phia = E0.isogeny(kernel=Ra, algorithm='factored', model='montgomery', check=False)
Ea = phia.codomain()

sb = randint(0, 3**b-1)
Rb = Pb + sb * Qb
phib = E0.isogeny(kernel=Rb, algorithm='factored', model='montgomery', check=False)

Ea, phia_Pb, phia_Qb = phia.codomain(), phia(Pb), phia(Qb)
Eb, phib_Pa, phib_Qa = phib.codomain(), phib(Pa), phib(Qa)


print(f'phib_Pa = {phib_Pa.xy()}')
print(f'phib_Qa = {phib_Qa.xy()}')

print(f'Ea: {Ea}')
print(f'Eb: {Eb}')

phib_Ra = phib_Pa + sa * phib_Qa
Eab = Eb.isogeny(kernel=phib_Ra, algorithm='factored', model='montgomery', check=False).codomain()
jab = Eab.j_invariant()

phia_Rb = phia_Pb + sb * phia_Qb
Eba = Ea.isogeny(kernel=phia_Rb, algorithm='factored', model='montgomery', check=False).codomain()
jba = Eba.j_invariant()

assert jab == jba
h = bytes_to_long(hashlib.sha256(str(jab).encode()).digest())
enc = h ^ bytes_to_long(flag)
print(f'enc = {enc}')


"""
Pa = (199176096138773310217268*ii + 230014803812894614137371, 21529721453350773259901*ii + 106703903226801547853572)
Qa = (8838268627404727894538*ii + 42671830598079803454272, 232086518469911650058383*ii + 166016721414371687782077)
Pb = (200990566762780078867585*ii + 156748548599313956052974, 124844788269234253758677*ii + 161705339892396558058330)
Qb = (39182754631675399496884*ii + 97444897625640048145787, 80099047967631528928295*ii + 178693902138964187125027)
phib_Pa = (149703758091223422379828*ii + 52711226604051274601866, 112079580687990456923625*ii + 147229726400811363889895)
phib_Qa = (181275595028116997198711*ii + 186563896197914896999639, 181395845909382894304538*ii + 69293294106635311075792)
Ea: Elliptic Curve defined by y^2 = x^3 + (11731710804095179287932*ii+170364860453198752624563)*x^2 + x over Finite Field in ii of size 232900919541184113672191^2
Eb: Elliptic Curve defined by y^2 = x^3 + (191884939246592021710422*ii+96782382528277357218650)*x^2 + x over Finite Field in ii of size 232900919541184113672191^2
enc = 48739425383997297710665612312049549178322149326453305960348697253918290539788
"""