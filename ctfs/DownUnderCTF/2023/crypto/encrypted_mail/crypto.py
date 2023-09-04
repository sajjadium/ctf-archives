import hashlib, secrets, random
from gmpy2 import powmod # faster than pow()
pow = lambda a, b, c: int(powmod(a, b, c))


g = 3
p = 1467036926602756933667493250084962071646332827366282684436836892199877831990586034135575089582195051935063743076951101438328248410785708278030691147763296367303874712247063207281890660681715036187155115101762255732327814001244715367


class Authenticator:
    def __init__(self, pubkey):
        self.y = pubkey

    def generate_challenges(self, n=128):
        challenges = []
        answers = []
        for _ in range(n):
            b = round(random.random())
            r = random.getrandbits(p.bit_length())
            c = random.getrandbits(p.bit_length())
            c1 = pow(g, r, p)
            if b == 0:
                c2 = pow(g, c, p)
            elif b == 1:
                c2 = pow(self.y, r, p)
            answers.append(b)
            challenges.append((int(c1), int(c2)))
        self.answers = answers
        return challenges

    def verify_answers(self, answers):
        return len(answers) == len(self.answers) and all(a == b for a, b in zip(answers, self.answers))


class Cipher:
    def __init__(self, key):
        self.n = 4
        self.idx = self.n
        self.state = [(key >> (32 * i)) & 0xffffffff for i in range(self.n)]

    def next(self):
        if self.idx == self.n:
            for i in range(self.n):
                x = self.state[i]
                v = x >> 1
                if x >> 31:
                    v ^= 0xa9b91cc3
                if x & 1:
                    v ^= 0x38ab48ef
                self.state[i] = v ^ self.state[(i + 3) % self.n]
            self.idx = 0

        v = self.state[self.idx]
        x0, x1, x2, x3, x4 = (v >> 31) & 1, (v >> 24) & 1, (v >> 18) & 1, (v >> 14) & 1, v & 1
        y = x0 + x1 + x2 + x3 + x4

        self.idx += 1
        return y & 1

    def next_byte(self):
        return int(''.join([str(self.next()) for _ in range(8)]), 2)

    def xor(self, A, B):
        return bytes([a ^ b for a, b in zip(A, B)])

    def encrypt(self, message):
        return self.xor(message, [self.next_byte() for _ in message])

    def decrypt(self, ciphertext):
        return self.xor(ciphertext, [self.next_byte() for _ in ciphertext])


class Encryptor:
    def __init__(self, public_key):
        self.public_key = public_key

    def encrypt(self, m):
        r = secrets.randbelow(p)
        c1 = pow(g, r, p)
        c2 = pow(self.public_key, r, p) * m % p
        return (c1, c2)


class Decryptor:
    def __init__(self, private_key):
        self.private_key = private_key

    def decrypt(self, ct):
        assert self.private_key is not None
        c1, c2 = ct
        m = c2 * pow(c1, -self.private_key, p) % p
        return m


class Signer:
    def __init__(self, private_key):
        self.private_key = private_key

    def hash(self, m):
        return int(hashlib.sha256(m).hexdigest(), 16)

    def sign(self, msg):
        k = secrets.randbelow(p-1) | 1
        r = pow(g, k, p)
        s = (self.hash(msg) - self.private_key * r) * pow(k, -1, p - 1) % (p - 1)
        return (r, s)


class Verifier:
    def __init__(self, public_key):
        self.public_key = public_key

    def hash(self, m):
        return int(hashlib.sha256(m).hexdigest(), 16)

    def verify(self, msg, sig):
        r, s = sig
        if not (0 < r < p and 0 < s < p - 1):
            return False
        return pow(g, self.hash(msg), p) == pow(self.public_key, r, p) * pow(r, s, p) % p


class Messenger:
    def __init__(self, private_key):
        self.private_key = private_key

    def send(self, recipient_public_key, message):
        key = secrets.randbelow(2**128)
        key_enc = Encryptor(recipient_public_key).encrypt(key)
        key_enc = key_enc[0].to_bytes(96, 'big') + key_enc[1].to_bytes(96, 'big')
        ct = Cipher(key).encrypt(message)
        sig = Signer(self.private_key).sign(ct)
        return (key_enc + ct, sig)

    def receive(self, sender_public_key, ciphertext, sig):
        if len(ciphertext) < 192:
            return False
        key_enc, ct = ciphertext[:192], ciphertext[192:]
        if not Verifier(sender_public_key).verify(ct, sig):
            return False
        key_enc0, key_enc1 = int.from_bytes(key_enc[:96], 'big'), int.from_bytes(key_enc[96:192], 'big')
        key = Decryptor(self.private_key).decrypt((key_enc0, key_enc1))
        message = Cipher(key).decrypt(ct)
        return message
