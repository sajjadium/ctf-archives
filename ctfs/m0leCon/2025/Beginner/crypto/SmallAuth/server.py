from secret import flag, password
import signal
from Crypto.Util.number import (
    bytes_to_long,
    long_to_bytes,
    getRandomRange,
)
from hashlib import sha256
import os

p = 5270716116965698502689689671130781219142402682027195438035167686031865721400130496197382604002325978977917823871038888373085118354500422489134429970793096193438377786459821943518301475690713718745453633483219759953295608491564410082912515903134742148257215875373630412689071144760281744294536079770426517968527527493218935968663682019557492826204481612047410320146277333682801905360248457200458458982939490478875010628228329816347137904546340745621643293109290190631986349878770000332829974864263568375989597228583046155053640478805958492876860588535257030218304135983005840752161675722091031537527270835889607480661582626985375282908187505873350960702103509549729997875801557977556414403796543012974965425751833424162010931383924392626875437842811285456196644742198291857617009931030974156758885265756942730260677252867252555430773014258836269996233420470473918801854039549216620237517053340745984578639983387808534554731327
assert len(password) > 64

def timeout_handler(_1, _2):
    raise TimeoutError


class AuthProtocol:
    def __init__(self, password: bytes):
        super().__init__()
        self.p = p
        self.g = pow(bytes_to_long(password), 2, self.p)

    def gen_pub_key(self):
        self.a = getRandomRange(2, self.p)
        self.A = pow(self.g, self.a, self.p)
        return self.A

    def gen_shared_key(self, B):
        assert 1 < B < self.p
        k = pow(B, self.a, self.p)
        self.s = sha256(long_to_bytes(k)).digest()
        return self.s

    def confirm_key(self):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(5)
        try:
            challenge = input("Give me the challenge (hex): ").strip()
            challenge = bytes.fromhex(challenge.strip())
            (opad, ipad, challenge) = challenge[:16], challenge[16:32], challenge[32:]
            if challenge == sha256(opad + sha256(ipad + self.s).digest()).digest():
                pad = bytes([x^y for x, y in zip(ipad, opad)])
                print("Response:", sha256(pad + self.s).hexdigest())
            else:
                print("Mmm, cannot understand this challenge.")
        except TimeoutError:
            ipad = os.urandom(16)
            opad = os.urandom(16)
            print("\nI got bored waiting for your response.")
            print("I will start then.")
            print(
                f"Here is your challenge: {opad.hex()}{ipad.hex()}{sha256(opad + sha256(ipad + self.s).digest()).hexdigest()}"
            )
            response = input("Response? (hex): ")
            try:
                response = bytes.fromhex(response.strip())
                pad = bytes([x^y for x, y in zip(ipad, opad)])
                if response == sha256(pad + self.s).digest():
                    return True
                else:
                    print("Nope sorry.")
            except Exception as e:
                print("Ops, error")
        except Exception as e:
            print("Ops, error")
        return False


def main():
    print(
        "Welcome! Please authenticate to get the flag. You should know the password, right?"
    )
    auth = AuthProtocol(password)

    print("Here is my public key:", auth.gen_pub_key())
    B = int(input("Give me your public key: "))
    auth.gen_shared_key(B)

    if auth.confirm_key():
        print("Welcome!", flag)


if __name__ == "__main__":
    main()
