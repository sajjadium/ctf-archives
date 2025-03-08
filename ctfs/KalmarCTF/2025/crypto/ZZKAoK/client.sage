import json

from intarg import Prover, Verifier, rel_factor

from server import check_proof

p = 7575421297630763282518938899604743465384629468827215656207919506716763809618505916447235217232727808548724534930629681051480532214588922728834440619141437
q = 8814446423351286610435906311084610082150929224828455307590664568123831451310506271910749908962699732322156406386518316597591762714288280144970264865581679
N = p * q

def prove(p, q):
    N = p * q
    prv = Prover(N)

    a = p**2 - 4
    b = q**2 - 4

    a1, a2, a3, a4 = four_squares(a)
    b1, b2, b3, b4 = four_squares(b)

    assert a1^2 + a2^2 + a3^2 + a4^2 == a
    assert b1^2 + b2^2 + b3^2 + b4^2 == b

    p = prv.com(p)
    q = prv.com(q)

    a1 = prv.com(a1)
    a2 = prv.com(a2)
    a3 = prv.com(a3)
    a4 = prv.com(a4)

    b1 = prv.com(b1)
    b2 = prv.com(b2)
    b3 = prv.com(b3)
    b4 = prv.com(b4)

    rel_factor(
        prv,
        p, a1, a2, a3, a4,
        q, b1, b2, b3, b4,
        N
    )

    pf = prv.finalize()

    return {
        'N': int(N),
        'pf': pf
    }

# generate a proof
msg = prove(p, q)

# sanity check proof
assert check_proof(msg) == p * q

# we can use this with the server :)
with open("example-proof.json", "w") as f:
    f.write(json.dumps(msg))
