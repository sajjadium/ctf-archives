import hashlib


def solve(challenge: str, difficulty: int) -> str:
    nonce = 0
    while nonce < 2**30:
        hash = hashlib.sha256((challenge + str(nonce)).encode()).digest()
        if int.from_bytes(hash, "big") >> (256 - difficulty) == 0:
            return str(nonce)
        nonce += 1
    raise RuntimeError("Could not find a nonce")
