from sage.all import *
from Crypto.Hash import keccak
from Crypto.Util.number import long_to_bytes, bytes_to_long
from struct import unpack
from random import SystemRandom
from json import loads, dumps

prng = SystemRandom()

def n2s(n):
    buf = long_to_bytes(n)
    return len(buf).to_bytes(8, 'big') + buf

def s2n(s):
    length = int.from_bytes(s[:8], 'big')
    return bytes_to_long(s[8:8+length]), s[8+length]

def serialize2bytes(*args) -> bytes:
    result = b''
    for arg in args:
        if isinstance(arg, bytes):
            result += arg
        elif isinstance(arg, int):
            result += n2s(arg)
        elif arg is None:
            pass
        elif isinstance(arg, list):
            result += n2s(len(arg))
            result += serialize2bytes(*arg)
        else:
            result += n2s(int(arg.xy()[0])) + n2s(int(arg.xy()[1]))
    return result

def H(*args):
    k = keccak.new(digest_bits=256)
    k.update(serialize2bytes(*args))
    return k.digest()

def Hn(n, *args):
    value = int.from_bytes(H(b'H_n', *args), 'big')
    return value % (n - 1) + 1

def Hp(E, G, *args):
    value = int.from_bytes(H(b'H_p', *args), 'big')
    q = E.base_field().order()
    x = value % (q - 1) + 1
    jump, iter = unpack('<QI', H(b'H_p_additional', *args)[:12])
    while True:
        pts = E.lift_x(x, all=True)
        if len(pts) > 0:
            candidate = pts[iter % len(pts)]
            if G.order() * candidate == E(0):
                return candidate
        x = (x - 1 + jump) % (q - 1) + 1

class OTRS(object):
    def __init__(self, E, G):
        self.E = E
        self.G = G
        self.n = G.order()
        self.q = E.base_field().order()

    def signature(self, Ks:list, m:bytes, k:int, bind_message=None, your_bind=None):
        K = k * self.G
        assert K in Ks
        n = len(Ks)
        assert bind_message is None or your_bind is not None
        if bind_message is None:
            pi = Ks.index(K)
        else:
            pi = list(zip(Ks, bind_message)).index((K, your_bind))
        I = k * Hp(self.E, self.G, K, None if bind_message is None else bind_message[pi])
        alpha = prng.randint(1, self.n - 1)
        Li = alpha * self.G
        Ri = alpha * Hp(self.E, self.G, K, None if bind_message is None else bind_message[pi])
        c_next = Hn(self.n, m, Li, Ri)
        r = [prng.randint(1, self.n - 1) for _ in range(n)]
        c_0 = None
        for i in list(range(pi + 1, n)) + list(range(0, pi)):
            if i == 0:
                c_0 = c_next
            Li = r[i] * self.G + c_next * Ks[i]
            Ri = r[i] * Hp(self.E, self.G, Ks[i], None if bind_message is None else bind_message[i]) + c_next * I
            c_next = Hn(self.n, m, Li, Ri)
        if c_0 is None:
            assert pi == 0
            c_0 = c_next
        r[pi] = alpha - c_next * k
        return (I, c_0, r)

    def verify(self, Ks:list, m:bytes, signature:tuple, bind_message=None):
        if len(Ks) == 0:
            return False
        I, c_0, r = signature
        c_next = c_0
        n = len(Ks)
        for i in range(n):
            Li = r[i] * self.G + c_next * Ks[i]
            Ri = r[i] * Hp(self.E, self.G, Ks[i], None if bind_message is None else bind_message[i]) + c_next * I
            c_next = Hn(self.n, m, Li, Ri)
        return c_next == c_0

class RangeProof(object):
    def __init__(self, otrs: OTRS, H=None):
        self.otrs = otrs
        self.E = otrs.E
        self.G = otrs.G
        self.n = otrs.n
        self.q = otrs.q
        if H is None:
            H = Hp(self.E, self.G, prng.randint(self.n * self.q))
        self.H = H

    def generate_commitment(self, x: int, r=None):
        if r is None:
            r = prng.randint(1, self.n - 1)
        C = r * self.G + x * self.H
        return (x, r, C)
    
    def verify_commitment(self, Ct: tuple):
        x, r, C = Ct
        return r * self.G + x * self.H == C
    
    def prove(self, Ct: tuple, n: int):
        assert n > 0
        assert self.verify_commitment(Ct)
        x, r, C = Ct
        hash_C = H(C)
        assert x < 2**n
        b = [ord(c) - 48 for c in bin(x)[2:].zfill(n)[::-1]]
        Cs = [self.generate_commitment(b[i] * 2**i) for i in range(n - 1)]
        last_r = (r - sum(r for x, r, C in Cs) % self.n + self.n) % self.n
        Cs.append(self.generate_commitment(b[n - 1] * 2**(n - 1), last_r))
        sigs = [self.otrs.signature([C, C - 2**i * self.H], hash_C, r) for i, (x, r, C) in enumerate(Cs)]
        Cs = [C for x, r, C in Cs]
        C_sum = Cs[0]
        for i in range(1, n):
            C_sum += Cs[i]
        assert C_sum == C
        return (Cs, sigs)

    def verify(self, C, n: int, proof:tuple):
        Cs, sigs = proof
        if not(len(Cs) == n == len(sigs)):
            return False
        C_sum = Cs[0]
        for i in range(1, n):
            C_sum += Cs[i]
        if C_sum != C:
            return False
        hash_C = H(C)
        return all([self.otrs.verify([C, C - 2**i * self.H], hash_C, sig) for i, (C, sig) in enumerate(zip(Cs, sigs))])

def serialize2json(*args):
    def s2d(v):
        if isinstance(v, tuple):
            return {"type": "tuple", "value": [s2d(i) for i in v]}
        elif isinstance(v, list):
            return {"type": "list", "value": [s2d(i) for i in v]}
        elif isinstance(v, set):
            return {"type": "set", "value": [s2d(i) for i in list(v)]}
        elif isinstance(v, int):
            return {"type": "int", "value": str(v)}
        elif isinstance(v, Integer):
            return {"type": "integer", "value": str(v)}
        elif isinstance(v, bytes):
            return {"type": "bytes", "value": v.hex()}
        elif isinstance(v, str):
            return {"type": "str", "value": v}
        elif isinstance(v, dict):
            return {"type": "dict", "value": [[s2d(key), s2d(value)] for key, value in v.items()]}
        else:
            return {"type": "point", "value": [str(v.xy()[0]), str(v.xy()[1])]}
    return dumps(s2d(args))

def deserialize4json(E, json):
    def d4d(v: dict):
        type_str = v['type']
        value = v['value']
        if type_str == "tuple":
            return (d4d(i) for i in value)
        elif type_str == "list":
            return [d4d(i) for i in value]
        elif type_str == "set":
            return set([d4d(i) for i in value])
        elif type_str == "int":
            return int(value)
        elif type_str == "integer":
            return Integer(int(value))
        elif type_str == "bytes":
            return bytes.fromhex(value)
        elif type_str == "dict":
            ret = dict()
            for [k, v] in value:
                ret[d4d(k)] = d4d(v)
            return ret
        elif type_str == "point":
            return E(int(value[0]), int(value[1]))
    return d4d(loads(json))

def curve_gen(q, a, gx, gy, n):
    Fq = GF(q)
    E = EllipticCurve(Fq, a)
    G = E(gx, gy)
    G.set_order(n)
    return (E, G)

def proof_curve():
    return curve_gen(16883071526461729727845365244775250968853779238387590508529343289688406548156898561121755709582605065974415626338418885206169694955938439285172466321629894047112152673890080193271092158984773170409123807574649665886686958584517, [16883071526461729727845365244775250968853779238387590508529343289688406548156898561121755709582605065974415626338418885206169694955938439285172466321629894047112152673890080193271092158984773170409123807574649665886686958584513, 50649214579385189183536095734325752906561337715162771525588029869065219644470695683365267128747815197923246879015256655618509084867815317855517398964889682141336458021670240579813276476954319511227371422723948997660060875753551], 14210586178493131406373190825820561003702506574011169828934446821536638945014471344113633023777761432403862087346540040982532990086531969109648355583610945828488439781287611999333627004372849450097379152416521048148055212429932, 7940930756869397961969852165330305368117788150170640034809962841577789648806280962338902036326685993547448607633972933475226268575544844316990777006161391199019112160116189041944360780606412770726712110640687030917392143404191, 129934874173417083152641070462750529831810853051271596159072328195848188613591686285280068379888878197177498309746)

def proof_H(E):
    return E(558502762260882368459100959026702189372961874916046935897584379942575091607773755509785872627683092849646763384923491591737048593593911906848644811657443277980186172014888060411213151459022266424905365693967579209745952778762, 5244497032739641374363689610162896907859634278068877212817118029249551959220656759501163866935794467197122778877280355210299933485519765003782178469195042075397340131431018419860106520716072042537547362606695008442528534605810)

def transaction_curve():
    return curve_gen(57896044618658097711785492504343953926634992332820282019728792003956564819949, [0, 486662, 0, 1, 0], 9, 14781619447589544791020593568409986887264606134616475288964881837755586237401, 7237005577332262213973186563042994240857116359379907606001950938285454250989)
