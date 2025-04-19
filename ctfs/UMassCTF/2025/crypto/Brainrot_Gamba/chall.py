from Crypto.Cipher import AES
from Crypto.Util.number import getStrongPrime, getRandomNBitInteger
import os
import json
import itertools

normal_deck = [''.join(card) for card in itertools.product("23456789TJQKA", "chds")]

# https://www.rfc-editor.org/rfc/rfc3526#section-3
p = int(""" FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
      29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
      EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
      E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
      EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
      C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
      83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
      670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF""".replace(' ', '').replace('\n', ''), 16)


def shuffle(l):
    return [x for x in sorted(l, key=lambda x: int.from_bytes(os.urandom(2)))]


def ghash(data, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    cipher.update(data)
    _, tag = cipher.encrypt_and_digest(b'')
    result = int.from_bytes(tag)
    if result < 1 << 127:
        result += 1 << 128
    return result ** 2


def encrypt(msg, e):
    return pow(msg, e, p)


def decrypt(msg, d):
    return pow(msg, d, p)


def random_key_pair():
    e = getRandomNBitInteger(p.bit_length() // 2) * 2 + 1
    d = pow(e, -1, p - 1)
    return e, d


def encrypt_deck(deck):
    e, d = random_key_pair()
    return d, [hex(encrypt(card, e)) for card in deck]


def decrypt_deck(deck, d):
    return [decrypt(int(card, 16), d) for card in deck]


def encrypt_cards(deck, hash_key, iv):
    keys = [random_key_pair() for _ in range(52)]
    return [key[1] for key in keys], [hex(encrypt(card, key[0])) for card, key in zip(deck, keys)], [
        hex(ghash(hex(key[1]).encode(), hash_key, iv)) for key in keys]


def decrypt_cards(card, my_key, opp_key, hash_key, hash_value, safely_hashed_deck, iv):
    opp_key = int(opp_key, 16)
    if hex(ghash(hex(opp_key).encode(), hash_key, iv)) != hash_value:
        raise ValueError("Your key has does not match your commitment!")
    decrypted = decrypt(decrypt(int(card, 16), opp_key), my_key)
    if decrypted not in safely_hashed_deck:
        raise ValueError("Your key does not decrypt correctly!")
    return safely_hashed_deck[decrypted]


def get_deck(msg, size):
    resp = input(msg)
    if len(resp) > 100000:
        raise ValueError("yeah i'm not parsing that.")
    deck = json.loads(resp)
    if not isinstance(deck, list):
        raise ValueError('You did not give me a list!')
    if len(deck) != size:
        raise ValueError("You did not give me the correct number of items!")
    if not all(isinstance(card, str) for card in deck):
        raise ValueError("You didn't give me valid items!")
    return deck


if __name__ == '__main__':
    hash_key = os.urandom(16)
    print(f"I commit to this key: {AES.new(hash_key, AES.MODE_ECB).encrypt(int.to_bytes(0, length=16)).hex()}")
    iv = bytes.fromhex(input("Please commit to an IV!"))
    deck = get_deck('Give me a deck of cards: ', 52)
    safely_hashed_deck = {ghash(bytes.fromhex(s), hash_key, iv): c for c, s in zip(normal_deck, shuffle(deck))}
    if len(safely_hashed_deck) != 52:
        raise ValueError("You didn't give me unique cards!")
    print(f"Here's the deck we're using: {json.dumps([hex(k) for k in safely_hashed_deck])}")
    print(f"You can check that the key I used matches my commitment: {hash_key.hex()}")

    print("Now, let's shuffle the deck!")
    global_d, deck = encrypt_deck(safely_hashed_deck)
    print(json.dumps(shuffle(deck)))
    deck = get_deck('Shuffle and encrypt, then give me back the deck: ', 52)
    deck = decrypt_deck(deck, global_d)
    my_keys, deck, key_hashes = encrypt_cards(deck, hash_key, iv)
    print(
        "I removed my global encryption, and added individual encryption. Here's my deck now, along with the hashes of the encryption: ")
    print(json.dumps(deck))
    print(json.dumps(key_hashes))
    deck = get_deck('Remove your global encryption, add your own individual encryption, then give me back the deck: ',
                    52)
    opponents_hashes = get_deck("Also, give me the hash to all your keys to make sure you're not cheating: ", 52)

    print("Now, let's play poker!")
    print("Here are the keys to your cards: ", json.dumps([hex(my_keys[i]) for i in [0, 1]]))
    opp_keys = get_deck("Give me my first two keys: ", 2)
    hand = {decrypt_cards(deck[i], my_keys[i], opp_keys[i - 2], hash_key, opponents_hashes[i], safely_hashed_deck, iv)
            for i in [2, 3]}
    if len(hand) < 2:
        raise ValueError("You didn't give me unique cards!")
    if not all(card[0] == 'A' for card in hand):
        raise ValueError("I'm not playing until I get aces!")

    print("Here are the keys to the streets: ", json.dumps([hex(my_keys[i]) for i in [4, 5, 6, 7, 8]]))
    opp_keys = get_deck("Give me my street keys: ", 5)
    street = {decrypt_cards(deck[i], my_keys[i], opp_keys[i - 4], hash_key, opponents_hashes[i], safely_hashed_deck, iv)
              for i in [4, 5, 6, 7, 8]}
    if len(street.union(hand)) < 7:
        raise ValueError("You didn't give me unique cards!")
    if not {'Ac', 'Ah', 'Ad', 'As'} <= street.union(hand):
        raise ValueError("I'm not betting until I get quad aces!")

    print("Here are the keys to my cards: ", json.dumps([hex(my_keys[i]) for i in [2, 3]]))
    print("Read em' and weep!")

    opp_keys = get_deck("Give me your first two keys: ", 2)
    opp_hand = {decrypt_cards(deck[i], my_keys[i], opp_keys[i], hash_key, opponents_hashes[i], safely_hashed_deck, iv)
                for i in [0, 1]}
    if len(street.union(opp_hand).union(hand)) < 9:
        raise ValueError("You didn't give me unique cards!")
    if not any({rank + suit for rank in 'TJQKA'} <= street.union(opp_hand) for suit in 'chds'):
        raise ValueError("I don't know what you think you had but it's clearly not beating aces!")

    print("dang, i should stop gambling.")
    with open('flag.txt', 'r') as f:
        print(f.readline())