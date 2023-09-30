import sys

sys.path.insert(1, 'SQISign-SageMath')

from SQISign import SQISign
import os

prover, verifier = SQISign(), SQISign()

# Generating key
prover.keygen()
EA = prover.export_public_key()
with open("public_key", "wb") as f:
    f.write(dumps(EA))

output_file = open("signatures.txt", "w")

print(f"EA_coeffs = {[EA.a4(), EA.a6()]}", file=output_file)


# Signing messages
msgs = ["Good", "luck"]
for i in range(2):

    E1, S = prover.sign(msgs[i].encode())

    print(f"E1{i}_coeffs = {[E1.a4(), E1.a6()]}", file=output_file)
    print(f"S{i} = '{S}'", file=output_file)
    assert verifier.verify(EA, (E1, S), msgs[i].encode())


