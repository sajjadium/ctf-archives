from ring_signature import proof_curve, RangeProof, OTRS, serialize2json, proof_H

E, G = proof_curve()
H = proof_H(E)

rp = RangeProof(OTRS(E, G), H)
Ct = rp.generate_commitment(__import__('secret').carol_pub[0])
x, r, C = Ct
proof = rp.prove(Ct, 256)
assert rp.verify(C, 256, proof)
with open("range_proof_from_carol.json", "w") as f:
    f.write(serialize2json(C, proof))
