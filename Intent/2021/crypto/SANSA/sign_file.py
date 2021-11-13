
from STARK.rescue_stark import rescue_sign
from STARK.rescue.rescue_hash import rescue
import yaml
from hashlib import blake2s
blake = lambda x: blake2s(x).digest()

PASSWORD = "<REDACTED>"
PASSWORD_HASH = [2019939026277137767,979901374969048238,1067125847181633502,445793449878813313]

def sign_file(path):
    """
    path: a file path to be signed

    returns signature - merkel_root1, merkel_root2, merkel_root3, merkel_branches1, merkel_branches2, merkel_branches3, low_degree_stark_proof
    """
    with open(path, "rb") as f:
        data = f.read()
    data_blake_hash = blake(data)
    file_hash = rescue([x for x in data_blake_hash])
    proof = rescue_sign([ord(x) for x in PASSWORD], PASSWORD_HASH, file_hash)

    proof_yaml = yaml.dump(proof, Dumper=yaml.SafeDumper)
    return proof_yaml
