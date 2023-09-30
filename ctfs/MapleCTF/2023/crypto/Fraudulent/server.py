from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
from secret import flag
from random import randint
from hashlib import sha256
import ast

def hash(values):
    h = sha256()
    for v in values:
        h.update(long_to_bytes(v))
    return bytes_to_long(h.digest())


def encrypt(m):
    assert 0 <= m < q
    y = randint(0, q - 1)
    s = pow(X, y, p)
    c_1 = pow(g, y, p)
    c_2 = pow(g, m, p) * s % p
    return (c_1, c_2)


def decrypt(c_1, c_2):
    s = pow(c_1, x, p)
    return c_2 * pow(s, -1, p) % p


# Return a count of votes for A
def get_votes():
    c_1 = 1
    c_2 = 1
    for vote in encrypted_votes_for_A:
        c_1 *= vote[0]
        c_2 *= vote[1]
    vote = decrypt(c_1, c_2)

    for i in range(10**4):
        if pow(g, i, p) == vote:
            return i
    return -1


# Verify that the encrypted_vote corresponds to either 0 or 1
def verify_vote(encrypted_vote, proof):
    R, S = encrypted_vote
    c_0, c_1, f_0, f_1 = proof

    values = [
        pow(g, f_0, p) * pow(R, -c_0, p) % p,
        pow(X, f_0, p) * pow(S, -c_0, p) % p,
        pow(g, f_1, p) * pow(R, -c_1, p) % p,
        pow(X, f_1, p) * pow(S, -c_1, p) * pow(g, c_1, p) % p,
    ]

    return c_0 + c_1 == hash(values)

p = 81561774084914804116542793383590610809004606518687125749737444881352531178029
g = 2
q = p - 1

# 1. Take in private key from user
x = int(input("Private key: "))
X = pow(g, x, p)

encrypted_votes_for_A = []

# 2. The server will encrypt 200 A votes and 150 B votes, then tally them
for i in range(200):
    encrypted_votes_for_A.append(encrypt(1))

for i in range(100):
    encrypted_votes_for_A.append(encrypt(0))


# 3. Now, you send a single ciphertext representing your vote
# Must also provide proof that your vote is either 0 or 1
encrypted_vote = ast.literal_eval(input("Vote (R, S): "))
proof = ast.literal_eval(input("Proof (C0, C1, F0, F1): "))

assert len(encrypted_vote) == 2 and len(proof) == 4
assert all([isinstance(k, int) for k in encrypted_vote])
assert all([isinstance(k, int) for k in proof])
assert verify_vote(encrypted_vote, proof), "Please vote for either 0 or 1."

# Tally all votes. If B has more votes, then you win
encrypted_votes_for_A.append(encrypted_vote)

votes_for_A = get_votes()
votes_for_B = 301 - votes_for_A

print("Votes for A:", votes_for_A)
print("Votes for B:", votes_for_B)

if votes_for_B > votes_for_A:
    print("You win!")
    print(flag)
else:
    print("So close! Next time.")
