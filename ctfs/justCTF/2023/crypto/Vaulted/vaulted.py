from coincurve import PublicKey
import json

FLAG = 'justWTF{th15M1ghtB34(0Rr3CtFl4G!Right????!?!?!??!!1!??1?}'
PUBKEYS = ['025056d8e3ae5269577328cb2210bdaa1cf3f076222fcf7222b5578af846685103', 
            '0266aa51a20e5619620d344f3c65b0150a66670b67c10dac5d619f7c713c13d98f', 
            '0267ccabf3ae6ce4ac1107709f3e8daffb3be71f3e34b8879f08cb63dff32c4fdc']


class FlagVault:
    def __init__(self, flag):
        self.flag = flag
        self.pubkeys = []

    def get_keys(self, _data):
        return str([pk.format().hex() for pk in self.pubkeys])

    def enroll(self, data):
        if len(self.pubkeys) > 3:
            raise Exception("Vault public keys are full")

        pk = PublicKey(bytes.fromhex(data['pubkey']))
        self.pubkeys.append(pk)
        return f"Success. There are {len(self.pubkeys)} enrolled"

    def get_flag(self, data):
        # Deduplicate pubkeys
        auths = {bytes.fromhex(pk): bytes.fromhex(s) for (pk, s) in zip(data['pubkeys'], data['signatures'])}

        if len(auths) < 3:
            raise Exception("Too few signatures")

        if not all(PublicKey(pk) in self.pubkeys for pk in auths):
            raise Exception("Public key is not authorized")

        if not all(PublicKey(pk).verify(s, b'get_flag') for pk, s in auths.items()):
            raise Exception("Signature is invalid")

        return self.flag


def write(data):
    print(json.dumps(data))


def read():
    try:
        return json.loads(input())
    except EOFError:
        exit(0)


WELCOME = """
Welcome to the vault! Thank you for agreeing to hold on to one of our backup keys.

The vault requires 3 of 4 keys to open. Please enroll your public key.
"""

if __name__ == "__main__":
    vault = FlagVault(FLAG)
    for pubkey in PUBKEYS:
        vault.enroll({'pubkey': pubkey})

    write({'message': WELCOME})
    while True:
        try:
            data = read()
            if data['method'] == 'get_keys': 
                write({'message': vault.get_keys(data)})
            elif data['method'] == 'enroll':
                write({'message': vault.enroll(data)})
            elif data['method'] == "get_flag":
                write({'message': vault.get_flag(data)})
            else:
                write({'error': 'invalid method'})
        except Exception as e:
            write({'error': repr(e)})
