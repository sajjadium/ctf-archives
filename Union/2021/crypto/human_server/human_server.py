import os, random, hashlib, textwrap, json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import getPrime, long_to_bytes


from fastecdsa.curve import secp256k1
from fastecdsa.point import Point

FLAG = b'union{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}'

CURVE = secp256k1
ORDER = CURVE.q
G = CURVE.G

class EllipticCurveKeyExchange():
    def __init__(self):
        self.private = random.randint(0,ORDER)
        self.public = self.get_public_key()
        self.recieved = None
        self.nonce = None
        self.key = None

    def get_public_key(self):
        A = G * self.private
        return A

    def send_public(self):
        return print(json.dumps({"Px" : self.public.x, "Py" : self.public.y}))

    def receive_public(self, data):
        """
        Remember to include the nonce for ultra-secure key exchange!
        """
        Px = int(data["Px"])
        Py = int(data["Py"])
        self.recieved = Point(Px, Py, curve=secp256k1)
        self.nonce = int(data['nonce'])

    def get_shared_secret(self):
        """
        Generates the ultra secure secret with added nonce randomness
        """
        assert self.nonce.bit_length() > 64
        self.key = (self.recieved * self.private).x ^ self.nonce

    def check_fingerprint(self, h2: str):
        """
        If this is failing, remember that you must send the SAME
        nonce to both Alice and Bob for the shared secret to match
        """
        h1 = hashlib.sha256(long_to_bytes(self.key)).hexdigest()
        return h1 == h2

    def send_fingerprint(self):
        return hashlib.sha256(long_to_bytes(self.key)).hexdigest()

def print_header(title: str):
    print('\n\n'+'*'*64+'\n'+'*'+title.center(62)+'*\n'+'*'*64+'\n\n')

def input_json(prompt: str):
    data = input(prompt)
    try:
        return json.loads(data)
    except:
        print({"error": "Input must be sent as a JSON object"})
        exit()

def encrypt_flag(shared_secret: int):
    iv = os.urandom(16)
    key = hashlib.sha1(long_to_bytes(shared_secret)).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))

    data = {}
    data['iv'] = iv.hex()
    data['encrypted_flag'] = ciphertext.hex()
    return print(json.dumps(data))


Alice = EllipticCurveKeyExchange()
Bob = EllipticCurveKeyExchange()

print_header('Welcome!') 
message = "Hello! Thanks so much for jumping in to help. Ever since everyone left WhatsApp, we've had a hard time keeping up with communications. We're hoping by outsourcing the message exchange to some CTF players we'll keep the load down on our servers... All messages are end-to-end encrypted so there's no privacy issues at all, we've even rolling out our new ultra-secure key exchange with enhanced randomness! Again, we really appreciate the help, feel free to add this experience to your CV!"
welcome = textwrap.fill(message, width=64)          
print(welcome)

print_header('Alice sends public key')
Alice.send_public()

print_header("Please forward Alice's key to Bob")
alice_to_bob = input_json('Send to Bob: ')
Bob.receive_public(alice_to_bob)

print_header('Bob sends public key')
Bob.send_public()

print_header("Please forward Bob's key to Alice")
bob_to_alice = input_json('Send to Bob: ')
Alice.receive_public(bob_to_alice)
            
Alice.get_shared_secret()
Bob.get_shared_secret()

print_header('Key verification in progress')
alice_happy = Alice.check_fingerprint(Bob.send_fingerprint())
bob_happy = Bob.check_fingerprint(Alice.send_fingerprint())
if not alice_happy or not bob_happy:
    print({"error": "Alice and Bob panicked: Potential MITM attack in progress!!"})
    exit()

print_header('Alice sends encrypted flag to Bob')
encrypt_flag(Alice.key)

