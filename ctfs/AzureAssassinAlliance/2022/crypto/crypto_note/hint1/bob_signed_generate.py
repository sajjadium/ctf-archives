from json import dump
from signed_message_verifier import SM2, get_bob_sign_pub
from secret import bob_priv

text = 'Bob: Do you remember the 1 token I lent you? Pay off that loan, now!'
signer = SM2(public_key=get_bob_sign_pub(), private_key=hex(bob_priv)[2:].zfill(64))
sign = signer.sign_with_sm3(text.encode())

dump([text, sign], open('signed_message_from_bob.json', 'w'))
