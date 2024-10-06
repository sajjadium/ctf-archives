from curve_operations import Point,Curve    # Custom module
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes

class Dual_EC:

    def __init__(self):
        p = 229054522729978652250851640754582529779
        a = -75
        b = -250
        self.curve = Curve(p,a,b)
        self.P = Point(97396093570994028423863943496522860154 , 2113909984961319354502377744504238189)
        self.Q = Point(137281564215976890139225160114831726699 , 111983247632990631097104218169731744696)
        self.set_initial_state()

    def set_initial_state(self):
        self.state = ???SECRET🤫???

    def set_next_state(self):
        self.state = self.curve.scalar_multiply(self.P, self.state).x

    def gen_rand_num(self):
        rand_point = self.curve.scalar_multiply(self.Q, self.state)
        rand_num = rand_point.x
        self.set_next_state()
        return rand_num

def main():
    prng = Dual_EC()
    flag = b'flag{test}'
    print("My PRNG has passed International Standards!!!")
    print("Here is a Sample Random Number to prove it to you : ", prng.gen_rand_num())
    key = long_to_bytes((prng.gen_rand_num() << 128) + prng.gen_rand_num())
    iv = long_to_bytes(prng.gen_rand_num())
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_bytes = cipher.encrypt(pad(flag, AES.block_size))
    print('Encrypted bytes : ',encrypted_bytes)

if(__name__ == "__main__"):
    main()