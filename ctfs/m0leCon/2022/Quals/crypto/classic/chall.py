from secret import flag
import random

def xor(s1, s2):
    res = ""
    for a, b in zip(s1, s2):
        res += str(int(a)^int(b))
    return res

class Classic(object):
    def __init__(self, rotors):
        self.rotors = rotors
        random.shuffle(self.rotors)
        self.perms = self.gen_permutations()

    def gen_permutations(self):
        res = {}
        start = [0,1,2,3]
        for i in range(16):
            tmp = start[:]
            x = bin(i)[2:].rjust(4,'0')
            for j in range(4):
                if x[j] == '0':
                    tmp[(-j)%4], tmp[(-1-j)%4] = tmp[(-1-j)%4], tmp[(-j)%4]
            res[x] = tmp
        return res

    def update_rotors(self):
        for i in range(len(self.rotors)):
            self.rotors[i] = self.rotors[i][1:]+[self.rotors[i][0]]

    def encrypt(self, plain):
        plain = plain.hex()
        k = list(range(16))
        v = [bin(i)[2:].rjust(4,'0') for i in range(16)]
        alph = '0123456789abcdef'
        ciphertext = ""
        for c in plain:
            xor_part = ''.join([str(rot[0]) for rot in self.rotors[:4]])
            perm_part = ''.join([str(rot[0]) for rot in self.rotors[4:]])
            enc = v[int(c,16)]
            xored = xor(enc, xor_part)
            ct = ''.join([str(xored[self.perms[perm_part][l]]) for l in range(4)])
            ciphertext += alph[v.index(ct)]
            self.update_rotors()
        return ciphertext

base_text = b"m0leCon 2022 is the fourth edition of the computer security conference organized by the student team pwnthem0le in collaboration with Politecnico di Torino. The aim is to bring together hackers, security experts, and IT specialists from different backgrounds and skill levels. The conference will feature a variety of talks and presentations, mostly focused on multiple aspects of offensive security. It will be entirely held in english."
to_encrypt = base_text+flag
rot = []

for l in [47, 53, 59, 61, 64, 65, 67, 69]:
    rot.append([random.randint(0,1) for _ in range(l)])

cipher = Classic(rot)
print(cipher.encrypt(to_encrypt))
