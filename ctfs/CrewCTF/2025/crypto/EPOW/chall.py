from sage.all import EllipticCurve, GF, os, is_prime

# Doing PoW's with elliptic curves!

Nm = 10

for TT in range(Nm):
    m = os.urandom(7)
    print(f"Entering proof #{TT + 1} of {Nm}, the salt is: {m.hex()}")
    X = bytes.fromhex(input("> "))
    A = int.from_bytes(X + m)
    p = int(input("> "))
    E = EllipticCurve(GF(p), [0, A, 0, 1, 0])
    assert len(X) == 1
    assert is_prime(p), "Are you kidding me?"
    assert p.bit_length() >= 384, "Too small! I can't be fooled like that!"
    assert p.bit_length() <= 640, "Too big! You'll fry my PC!"
    assert E.is_supersingular(), "You failed the proof!"

print("All levels were passed! You deserve a flag for your effort!")
print(open("flag.txt").read())
