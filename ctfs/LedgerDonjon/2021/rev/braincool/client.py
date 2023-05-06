import requests

CHALLENGE_URL = "http://braincool.donjon-ctf.io:3200/apdu"


def get_public_key():
    req = requests.post(CHALLENGE_URL, data=bytes.fromhex("e005000000"))
    response = req.content
    if response[-2:] != b"\x90\x00":
        return None
    return response[:-2]


public_key = get_public_key()
assert public_key == bytes.fromhex("0494e92dd2a82e93d90c13322819db091a869c30c03c5a47d7b1f38683ba9bfdf33f44582dbd19e55e319ce5b2929fba6da9705c84df8c209441bcb713cf99c6d5d6e94445bc808e6821b73f3fa7d55b8a")
