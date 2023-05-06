from STARK.rescue_stark import rescue_verify
from STARK.rescue.rescue_hash import rescue
import yaml
from hashlib import blake2s
from logging import *

blake = lambda x: blake2s(x).digest()

PASSWORD_HASH = [2019939026277137767,979901374969048238,1067125847181633502,445793449878813313]

def verify_file(path, signature):
    with open(path, "rb") as f:
        data = f.read()
    return verify_data(data, signature)

def verify_data(data, signature):
    try:
        signature = yaml.load(signature, Loader=yaml.SafeLoader)
    except Exception as e:
        return False
    data_blake_hash = blake(data)
    file_hash = rescue([x for x in data_blake_hash])
    return rescue_verify(PASSWORD_HASH, signature, file_hash, 18, 4096)

    