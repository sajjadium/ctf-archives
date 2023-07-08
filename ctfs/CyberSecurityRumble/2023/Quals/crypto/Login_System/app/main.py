import os
from flag import FLAG
from bplib.bp import BpGroup, G1Elem, G2Elem

USER = {}

### Signature

def setup():
    G = BpGroup()
    g1, g2 = G.gen1(), G.gen2()
    e, o = G.pair, G.order()
    return (G, o, g1, g2, e)

def keygen():
    (G, o, g1, g2, e) = PARAMS
    x = o.random()
    return (x, x*g2)

def sign(sk, m):
    (G, o, g1, g2, e) = PARAMS
    h = G.hashG1(m)
    return sk * h

def verify(pk, m, sig):
    (G, o, g1, g2, e) = PARAMS
    h = G.hashG1(m)
    return e(sig, g2) == e(h, pk)

def aggregate_signatures(signatures):
    result = signatures[0]
    for sig in signatures[1:]:
        result += sig

    return result

def verify_aggregated_signature(pks, messages, sig):
    (G, o, g1, g2, e) = PARAMS
    
    result = e(G.hashG1(messages[0]), pks[0])
    for pk, message in zip(pks[1:], messages[1:], strict=True):
        result *= e(G.hashG1(message), pk)

    return e(sig, g2) == result


### Logic

def print_menu():
    print("""[1] Register user
[2] Log into admin interface
[3] Exit
    """)

def register_user():
    (G, o, g1, g2, e) = PARAMS

    username = input('Username: ')

    if username in USER:
        print("Username already taken")
        return

    pubkey = input('Pubkey: ').strip()
    pubkey = G2Elem.from_bytes(bytes.fromhex(pubkey), G)

    USER[username] = pubkey

def login():
    (G, o, g1, g2, e) = PARAMS

    username = input('Username: ')

    print("To log in pls provide a valid signature for the following challenge with your key and the key of the admin")

    challenge = os.urandom(32).hex()

    print(f"Challenge: {challenge}")

    sig = input('Sig: ').strip()
    sig = G1Elem.from_bytes(bytes.fromhex(sig), G)

    if verify_aggregated_signature([ADMIN_PK, USER[username]], [challenge.encode()] * 2, sig):
        print(FLAG)
    else:
        print("Nope")




if __name__ == '__main__':
    global ADMIN_PK, PARAMS

    PARAMS = setup()
    (G, o, g1, g2, e) = PARAMS
    # The paringgroup G generated is always the same
    print(f"G1: {g1.export().hex()}")
    print(f"G2: {g2.export().hex()}")
    # e = G.pair(g1, g2)

    # Test
    sk, pk = keygen()
    sig = sign(sk, b"Foo")
    assert verify(pk, b"Foo", sig)

    sk2, pk2 = keygen()
    sig2 = sign(sk2, b"Bar")

    aggregated_sig = aggregate_signatures([sig, sig2])

    assert verify_aggregated_signature([pk, pk2], [b"Foo", b"Bar"], aggregated_sig)

    _, ADMIN_PK = keygen()
    print(f"Admin public key: {ADMIN_PK.export().hex()}")

    while True:
        print_menu()
        option = int(input("> "))
        if option == 1:
            register_user()
        elif option == 2:
            login()
        else:
            break