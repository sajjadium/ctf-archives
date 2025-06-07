from tinyec.ec import SubGroup, Curve
from RMT import R_MT19937_32bit as special_random
from decor import HP, death_message, menu_box, title_drop
from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random.random import getrandbits
from hashlib import sha256
from json import loads
import sys
import os
from secret import FLAG

CORE = 0xb4587f9bd72e39c54d77b252f96890f2347ceff5cb6231dfaadb94336df08dfd


class _1000_THR_Signing_System:
    def __init__(self):
        # secp256k1 
        self.p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
        self.a = 0x0000000000000000000000000000000000000000000000000000000000000000
        self.b = 0x0000000000000000000000000000000000000000000000000000000000000007
        self.Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        self.Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
        self.n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
        self.h = 0x1

        subgroup = SubGroup(self.p, (self.Gx, self.Gy), self.n, self.h)
        self.curve = Curve(self.a, self.b, subgroup, name="CustomCurve")

        self.cinit = 0
        self.d = self.privkey_gen()
        self.P = self.curve.g
        self.Q = self.d * self.P

        self.Max_Sec = special_random(getrandbits(32))

    def sec_real_bits(self,bits: int) -> int:
        if bits % 32 != 0:
            raise ValueError("Bit length must be a multiple of 32")   
        exp = bits // 32
        x = self.Max_Sec.get_num() ** exp
        cyc_exhausted = 0
        while x.bit_length() != bits:
            x = self.Max_Sec.get_num() ** exp
            cyc_exhausted += 1
        return (x, cyc_exhausted)  
    
    @staticmethod
    def real_bits(bits) -> int:
        x = getrandbits(bits)
        while x.bit_length() != bits:
            x = getrandbits(bits)
        return x

    @staticmethod
    def supreme_RNG(seed: int, length: int = 10):
        while True:
            str_seed = str(seed) if len(str(seed)) % 2 == 0 else '0' + str(seed)
            sqn = str(seed**2)
            mid = len(str_seed) >> 1
            start = (len(sqn) >> 1) - mid
            end = (len(sqn) >> 1) + mid   
            yield sqn[start : end].zfill(length)
            seed = int(sqn[start : end])  
    
    def restart_level(self):
        print("S T A R T I N G  R O U T I N E . . .\n")

        self.Max_Sec = special_random(getrandbits(32))

        self.d = self.privkey_gen()
        self.P = self.curve.g
        self.Q = self.d * self.P
       
    def sign(self, msg: bytes) -> tuple:
        k, n1, n2, cycles = self.full_noncense_gen() # 全くナンセンスですが、日本語では
        
        kG = k * self.P
        r = kG.x % self.n
        k = k % self.n
        Hmsg = sha256()
        Hmsg.update(msg)

        s = ((b2l(Hmsg.digest()) + r * self.d) * pow(k, -1, self.n)) % self.n

        return (r, s, n1, n2, cycles)
    
    def partial_noncense_gen(self,bits: int, sub_bits: int, shift: int) -> int:
        term = self.real_bits(bits)
        _and = self.real_bits(bits - sub_bits)
        equation = term ^ ((term << shift) & _and) 
        return (term,_and,equation)


    def full_noncense_gen(self) -> tuple:
        k_m1 = self.real_bits(24)
        k_m2 = self.real_bits(24) 
        k_m3 = self.real_bits(69) 
        k_m4 = self.real_bits(30) 

        k_, cycle_1 = self.sec_real_bits(32)
        _k, cycle_2 = self.sec_real_bits(32)

        benjamin1, and1, eq1 = self.partial_noncense_gen(32, 16, 16)
        benjamin2, and2, eq2 = self.partial_noncense_gen(32 ,16 ,16)

        const_list = [k_m1, (benjamin1 >> 24 & 0xFF), k_m2, (benjamin1 >> 16 & 0xFF) , k_, (benjamin1 >> 8 & 0xFF), k_m3, (benjamin1 & 0xFF), k_m4, (benjamin2 >> 24 & 0xFFF), _k]
        shift_list = [232, 224, 200, 192, 160, 152, 83, 75, 45, 33, 0]

        n1 = [and1, eq1]
        n2 = [and2, eq2]
        cycles = [cycle_1, cycle_2]

        noncense = 0
        for const, shift in zip(const_list, shift_list):
            noncense += const << shift
        return noncense, n1, n2, cycles   


    def privkey_gen(self) -> int:
        simple_lcg = lambda x: (x * 0xeccd4f4fea74c2b057dafe9c201bae658da461af44b5f04dd6470818429e043d + 0x8aaf15) % self.n

        if not self.cinit:
            RNG_seed = simple_lcg(CORE)
            self.n_gen = self.supreme_RNG(RNG_seed)
            RNG_gen = next(self.n_gen)
            self.cinit += 1
        else:
            RNG_gen = next(self.n_gen)               

        p1 = hex(self.real_bits(108))
        p2 = hex(self.real_bits(107))[2:]

        priv_key = p1 + RNG_gen[:5] + p2 + RNG_gen[5:]

        return int(priv_key, 16)
    
    def gen_encrypted_flag(self) -> tuple:
        sha2 = sha256()
        sha2.update(str(self.d).encode('ascii'))
        key = sha2.digest()[:16]
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(FLAG, 16))
        return (ciphertext.hex(), iv.hex())
            
    def _dead_coin_params(self) -> tuple:
        base = 2
        speed = getrandbits(128)
        feedbacker_parry = int(next(self.n_gen))
        style_bonus = feedbacker_parry ^ (feedbacker_parry >> 5)
        power = pow(base, style_bonus, speed)
        return (power, speed, feedbacker_parry)
    
    def deadcoin_verification(self, tries):

        if tries < 3:
            print(f"Successfully perform a {"\33[33m"}deadcoin{"\33[0m"} and perform a {"\33[34m"}feedbacker{"\33[0m"} parry for getting {"\33[1;91m"}BLOOD{"\33[0m"} to survive.\n")
            power, speed, feedbacker_parry = self._dead_coin_params()
            print(f"Calculated power and speed for the number - {tries+1} deadcoin: {power, speed}")
            try:
                action_code = int(input("Action code: "))
                if action_code == feedbacker_parry:
                    blood = self.Max_Sec.get_num()
                    print(f"[+ FISTFUL OF DOLLAR]")
                    print(f"Here's some {"\33[1;91m"}BLOOD{"\33[0m"} - ID: {blood}")
                    return True
                else:
                    print("Missed.")
            except:
                print("Invalid action code")
        else:
            print("You're done.")
        return False


class _1000_THR_EARTHMOVER:
    def __init__(self):
        self.Boss = _1000_THR_Signing_System()

    def get_encrypted_flag(self):
        ciphertext, iv = self.Boss.gen_encrypted_flag()   
        return {"ciphertext": ciphertext,"iv": iv}      
    
    def perform_deadcoin(self, tries):
        return self.Boss.deadcoin_verification(tries)

    def call_the_signer(self):
        msg = input("What do you wish to speak? ").encode()
        r, s, n1, n2, cycles = self.Boss.sign(msg)
        return {"r": r, "s": s, "nonce_gen_consts": [n1, n2], "heat_gen": cycles}

    def level_restart(self):
        self.Boss.restart_level()
    
    def level_quit(self):
        sys.exit()
    
   
def main():
    from time import sleep
    LEVEL = _1000_THR_EARTHMOVER()
    tries = 0
    title_drop()


    V1 = HP(100,100, "V1", HP.color_red)

    while True:
        try:
            menu_box()
            print(f'\n{V1}')
            move = loads(input("\nExpecting Routine in JSON format: "))

            if "event" not in move:
                print({"Error": "Unrecognised event"})
                continue

            v1_action = move["event"]

            survive = V1.check(v1_action)
            if not survive:
                death_message()
                break

            if v1_action == "get_encrypted_flag":
                print(LEVEL.get_encrypted_flag())
                V1.update(V1.current_health-50)

            elif v1_action == "perform_deadcoin":
                verify = LEVEL.perform_deadcoin(tries)
                tries += 1
                if verify:
                    V1.update(V1.current_health+20)

            elif v1_action == "call_the_signer":
                print(LEVEL.call_the_signer())
                V1.update(V1.current_health-20)

            elif v1_action == "level_restart":
                LEVEL.level_restart()
                V1.update(100)

            elif v1_action == "level_quit":
                LEVEL.level_quit()

            else:
                print({"Error": "Unrecognised V1 action"})

        except Exception as e:
            print({"Error": str(e)})

        
if __name__ == "__main__":
    main()

