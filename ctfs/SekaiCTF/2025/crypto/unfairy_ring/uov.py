#   uov.py
#   2024-04-24  Markku-Juhani O. Saarinen <mjos@iki.fi>. See LICENSE

#   === Implementation of UOV 1.0 ===

from Crypto.Cipher import AES
from Crypto.Hash import SHAKE256
import os

class UOV:

    #   initialize
    def __init__(self, gf=256, n=112, m=44, pkc=False, skc=False, name='',
                        rbg=os.urandom):
        """ Initialize the class with UOV parameters. """
        self.gf     =   gf                  #   _GFSIZE
        self.n      =   n                   #   _PUB_N
        self.m      =   m                   #   _PUB_M
        self.v      =   n - m               #   _V
        self.pkc    =   pkc                 #   public key compression
        self.skc    =   skc                 #   secret key compression
        self.name   =   name                #   spec name
        self.rbg    =   rbg                 #   randombytes() callback

        if pkc:                             #   variant names as in KAT files
            kc = 'pkc'                      #   spec uses pkc/skc, KAT cpk/csk
        else:
            kc = 'classic'
        if skc:
            kc += '-skc'
        self.katname    =   f'OV({gf},{n},{m})-{kc}'

        if self.gf == 256:                  #   two kinds of Finite fields
            self.gf_bits    =   8
            self.gf_mul     =   self.gf256_mul
            self.gf_mulm    =   self.gf256_mulm
        elif self.gf == 16:
            self.gf_bits    =   4
            self.gf_mul     =   self.gf16_mul
            self.gf_mulm    =   self.gf16_mulm
        else:
            raise   ValueError

        self.v_sz   =   self.gf_bits * self.v // 8  #   _V_BYTE
        self.n_sz   =   self.gf_bits * self.n // 8  #   _PUB_N_BYTE
        self.m_sz   =   self.gf_bits * self.m // 8  #   _PUB_M_BYTE, _O_BYTE

        self.seed_sk_sz =   32              #   LEN_SKSEED
        self.seed_pk_sz =   16              #   LEN_PKSEED
        self.salt_sz    =   16              #   _SALT_BYTE

        #   bit mask for "mulm" multipliers
        mm = 0
        for i in range(self.m):
            mm = self.gf * mm + (self.gf >> 1)
        self.mm     = mm

        #   external sizes
        def triangle(n):
            return n * (n + 1) // 2
        self.sig_sz =   self.n_sz + self.salt_sz        #   OV_SIGNATUREBYTES
        self.so_sz  =   self.m * self.v_sz              #

        self.p1_sz  =   self.m_sz * triangle(self.v)    #   _PK_P1_BYTE
        self.p2_sz  =   self.m_sz * self.v * self.m     #   _PK_P2_BYTE
        self.p3_sz  =   self.m_sz * triangle(self.m)    #   _PK_P3_BYTE

        if  self.pkc:
            self.pk_sz  =   self.seed_pk_sz + self.p3_sz            #   |cpk|
        else:
            self.pk_sz  =   self.p1_sz + self.p2_sz + self.p3_sz    #   |epk|

        if  self.skc:
            self.sk_sz  =   self.seed_sk_sz                         #   |csk|
        else:
            self.sk_sz  =   (   self.seed_sk_sz + self.so_sz +      #   |esk|
                                self.p1_sz  +   self.p2_sz  )

    #   random & symmetric crypto hooks

    def set_random(self, rbg):
        """ Set the key material RBG."""
        self.rbg        =   rbg

    def shake256(self, x, l):
        """ shake256s(x, l): Internal hook."""
        return SHAKE256.new(x).read(l)

    def aes128ctr(self, key, l, ctr=0):
        """ aes128ctr(key, l): Internal hook."""
        iv      =   b'\x00' * 12
        aes     =   AES.new(key, AES.MODE_CTR, nonce=iv, initial_value=ctr)
        return  aes.encrypt(b'\x00' * l)

    #   basic finite field arithmetic

    def gf16_mul(self, a, b):
        """ GF(16) multiply: a*b mod (x^4 + x + 1). """
        r = a & (-(b & 1))
        for i in range(1, 4):
            t = a & 8
            a = ((a ^ t) << 1) ^ (t >> 2) ^ (t >> 3)
            r ^= a & (-((b >> i) & 1))
        return r

    def gf16_mulm(self, v, a):
        """ Vector (length m) * scalar multiply in GF(16). """
        r = v & (-(a & 1))
        for i in range(1, 4):
            t = v & self.mm
            v = ((v ^ t) << 1) ^ (t >> 3) ^ (t >> 2)
            if (a >> i) & 1:
                r ^= v
        return r

    def gf256_mul(self, a, b):
        """ GF(256) multiply: a*b mod (x^8 + x^4 + x^3 + x + 1). """
        r = a & (-(b & 1));
        for i in range(1, 8):
            a = (a << 1) ^ ((-(a >> 7)) & 0x11B);
            r ^= a & (-((b >> i) & 1));
        return r

    def gf256_mulm(self, v, a):
        """ Vector (length m) * scalar multiply in GF(256). """
        r = v & (-(a & 1))
        for i in range(1, 8):
            t = v & self.mm
            v = ((v ^ t) << 1) ^ (t >> 7) ^ (t >> 6) ^ (t >> 4) ^ (t >> 3)
            if (a >> i) & 1:
                r ^= v
        return r

    def gf_inv(self, a):
        """ GF multiplicative inverse: a^-1."""
        r = a       #   computes 2^14 or a^254 == a^-1
        for _ in range(2, self.gf_bits):
            a = self.gf_mul(a, a)
            r = self.gf_mul(r, a)
        r = self.gf_mul(r, r)
        return r

    #   serialization helpers

    def gf_pack(self, v):
        """ Pack a vector of GF elements into bytes. """
        if self.gf == 256:
            return bytes(v)
        elif self.gf == 16:
            return bytes( [ v[i] + (v[i + 1] << 4) for
                                i in range(0, len(v), 2) ] )

    def gf_unpack(self, b):
        """ Unpack bytes into a vector of GF elements """
        if self.gf == 256:
            return bytearray(b)
        elif self.gf == 16:
            v = []
            for x in b:
                v += [ x & 0xF, x >> 4 ]
            return bytearray(v)

    def unpack_mtri(self, b, d):
        """ Unpack an (upper) triangular matrix."""
        m = [ [ 0 ] * d for i in range(d) ]
        p = 0
        for i in range(d):
            for j in range(i, d):
                m[i][j] = int.from_bytes( b[ p : p + self.m_sz ] )
                p += self.m_sz
        return m

    def pack_mtri(self, m, d):
        """ Pack an upper triangular matrix."""
        b = b''
        for i in range(d):
            for j in range(i, d):
                t = m[i][j]
                b += t.to_bytes(self.m_sz)
        return b

    def unpack_mrect(self, b, h, w):
        """ Unpack a rectangular matrix."""
        m = [ [ 0 ] * w for i in range(h) ]
        p = 0
        for i in range(h):
            for j in range(w):
                m[i][j] = int.from_bytes( b[ p : p + self.m_sz ] )
                p += self.m_sz
        return m

    def pack_mrect(self, m, h, w):
        """ Pack a rectangular matrix."""
        b = b''
        for i in range(h):
            for j in range(w):
                b += m[i][j].to_bytes(self.m_sz)
        return b

    def unpack_rect(self, b, h, w):
        """ Unpack a rectangular matrix."""
        if self.gf == 256:
            m = [ b[i : i + w] for i in range(0, h * w, w) ]
        elif self.gf == 16:
            w_sz = w // 2
            m = [   self.gf_unpack(b[i : i + w_sz])
                        for i in range(0, h * w_sz, w_sz) ]
        return m

    #   === UOV internal arithmetic =========================================

    def calc_f2_p3(self, p1, p2, so):

        #   extract p1 (tri) and p2 (rectangular)
        m1 = self.unpack_mtri(p1, self.v)
        m2 = self.unpack_mrect(p2, self.v, self.m)
        mo = self.unpack_rect(so, self.m, self.v)

        #   create p3
        m3 = [ [ 0 ] * self.m for i in range(self.m) ]
        for j in range(self.m):
            for i in range(self.v):
                t = m2[i][j]
                for k in range(i, self.v):
                    t ^= self.gf_mulm( m1[i][k], mo[j][k] )
                for k in range(self.m):
                    u  = self.gf_mulm( t, mo[k][i] )
                    if j < k:
                        m3[j][k] ^= u
                    else:
                        m3[k][j] ^= u

        #   create sks in place of m2
        for i in range(self.v):
            for j in range(self.m):
                t = m2[i][j]
                for k in range(i + 1):
                    t ^= self.gf_mulm( m1[k][i], mo[j][k] )
                for k in range(i, self.v):
                    t ^= self.gf_mulm( m1[i][k], mo[j][k] )
                m2[i][j] = t

        #   fold and collect p3 (tri)
        p3 = self.pack_mtri(m3, self.m)

        #   collect sks (rect)
        sks = self.pack_mrect(m2, self.v, self.m)

        return (sks, p3)

    def gauss_solve(self, l, c):
        """ Solve a system of linear equations in GF."""

        #   system of linear equations:
        #   transpose and add constant on right hand side
        h   =   self.m
        w   =   self.m + 1
        l   =   [ self.gf_unpack( x.to_bytes(self.m_sz) ) for x in l ]
        m   =   [ [l[i][j] for i in range(h)] + [c[j]]
                            for j in range(h) ]

        #   gaussian elimination -- create a diagonal matrix on left
        for i in range(h):
            j = i
            while m[j][i] == 0:
                j += 1
                if j == h:
                    return None
            if i != j:
                for k in range(w):
                    m[i][k] ^= m[j][k]
            x = self.gf_inv( m[i][i] )
            for k in range(w):
                m[i][k] = self.gf_mul( m[i][k], x )
            for j in range(h):
                x = m[j][i]
                if j != i:
                    for k in range(w):
                        m[j][k] ^=  self.gf_mul(m[i][k], x)

        #   extract the solution (don't pack)
        return [ m[i][w - 1] for i in range(h) ]


    def pubmap(self, z, tm):
        """ Apply public map to z."""
        v   = self.v
        m   = self.m

        #   unserialize
        m1  = self.unpack_mtri(tm, v)
        m2  = self.unpack_mrect(tm[self.p1_sz:], v, m)
        m3  = self.unpack_mtri(tm[self.p1_sz + self.p2_sz:], m)
        x   = self.gf_unpack(z)

        y = 0   #   result
        #   P1
        for i in range(v):
            for j in range(i, v):
                y ^= self.gf_mulm(m1[i][j], self.gf_mul(x[i], x[j]))

        #   P2
        for i in range(v):
            for j in range(m):
                y ^= self.gf_mulm(m2[i][j], self.gf_mul(x[i], x[v + j]))

        #   P3
        for i in range(m):
            for j in range(i, m):
                y ^= self.gf_mulm(m3[i][j], self.gf_mul(x[v + i], x[v + j]))

        return y.to_bytes(self.m_sz)

    def expand_p(self, seed_pk):
        """ UOV.ExpandP(). """
        pk          =   self.aes128ctr(seed_pk, self.p1_sz + self.p2_sz);
        return          (pk[0:self.p1_sz], pk[self.p1_sz:])

    def expand_pk(self, cpk):
        """ UOV.ExpandPK(cpk). """
        seed_pk     =   cpk[:self.seed_pk_sz]
        p3          =   cpk[self.seed_pk_sz:]
        (p1, p2)    =   self.expand_p(seed_pk)
        epk         =   p1 + p2 + p3
        return      epk

    def expand_sk(self, csk):
        """ UOV.ExpandSK(csk). """
        seed_sk     =   csk[:self.seed_sk_sz]
        seed_pk_so  =   self.shake256(seed_sk, self.seed_pk_sz + self.so_sz)
        seed_pk     =   seed_pk_so[:self.seed_pk_sz]
        so          =   seed_pk_so[self.seed_pk_sz:]
        (p1, p2)    =   self.expand_p(seed_pk)
        (sks, p3)   =   self.calc_f2_p3(p1, p2, so)
        esk         =   seed_sk + so + p1 + sks
        return      esk

    #   === external / kat test api =========================================

    def keygen(self):
        """ UOV.classic.KeyGen(). """

        seed_sk     =   self.rbg(self.seed_sk_sz)
        seed_pk_so  =   self.shake256(seed_sk, self.seed_pk_sz + self.so_sz)
        seed_pk     =   seed_pk_so[:self.seed_pk_sz]
        so          =   seed_pk_so[self.seed_pk_sz:]
        (p1, p2)    =   self.expand_p(seed_pk)
        (sks, p3)   =   self.calc_f2_p3(p1, p2, so)

        #   public key compression
        if  self.pkc:
            pk  =   seed_pk + p3                #   cpk
        else:
            pk  =   p1 + p2 + p3                #   epk

        #   secret key compression
        if  self.skc:
            sk  =   seed_sk                     #   csk
        else:
            sk  =   seed_sk + so + p1 + sks     #   esk

        return (pk, sk)

    def sign(self, msg, sk):
        """ UOV.Sign()."""

        #   unpack secret key if necessary
        if self.skc:
            sk = self.expand_sk(sk)

        #   separate components
        j   =   self.seed_sk_sz
        seed_sk =   sk[ : self.seed_sk_sz ]
        so  =   sk[ self.seed_sk_sz :
                    self.seed_sk_sz + self.so_sz ]
        p1  =   sk[ self.seed_sk_sz + self.so_sz :
                    self.seed_sk_sz + self.so_sz + self.p1_sz ]
        sks =   sk[ self.seed_sk_sz + self.so_sz + self.p1_sz :
                    self.seed_sk_sz + self.so_sz + self.p1_sz + self.p2_sz ]

        #   deserialization
        mo  =   [ self.gf_unpack( so[i : i + self.v_sz] )
                    for i in range(0, self.so_sz, self.v_sz) ]
        m1  =   self.unpack_mtri(p1, self.v)
        ms  =   self.unpack_mrect(sks, self.v, self.m)

        #   1:  salt <- {0, 1}^salt_len
        salt    =   self.rbg(self.salt_sz)

        #   2:  t <- hash( mu || salt )
        t   =   self.shake256(msg + salt, self.m_sz)

        #   3:  for ctr = 0 upto 255 do
        ctr =   0
        x   =   None
        while x == None and ctr < 0x100:
            #   4:  v := Expand_v(mu || salt || seed_sk || ctr)
            v   =   self.gf_unpack(self.shake256(
                            msg + salt + seed_sk + bytes([ctr]), self.v_sz))
            ctr +=  1

            #   5:  L := 0_{m*m}
            ll  =   [ 0 ] * self.m

            #   6:  for i = 1 upto m do
            for i in range(self.m):

            #   7:      Set i-th row of L to v^T S_i
                for j in range(self.v):
                    ll[i] ^= self.gf_mulm(ms[j][i], v[j])

            #   9:      y <- v^t * Pi^(1) * v
            #   10:     Solve Lx = t - y for x

            #   "evaluate P1 with the vinegars"
            r = int.from_bytes(t)
            for i in range(self.v):
                u = 0
                for j in range(i, self.v):
                    u ^= self.gf_mulm( m1[i][j], v[j] )
                r ^= self.gf_mulm( u, v[i] )
            r = self.gf_unpack(r.to_bytes(self.m_sz))

            x = self.gauss_solve(ll, r)

        #   y = O * x
        y = bytearray(v)        #   subtract from v
        for i in range(self.m):
            for j in range(self.v):
                y[j] ^= self.gf_mul(mo[i][j], x[i])

        #   construct signature
        sig = self.gf_pack(y) + self.gf_pack(x) + salt

        return  sig


    def verify(self, sig, msg, pk):
        """ UOV.Verify() and UOV.pkc.Verify(). Return boolean if valid. """

        #   unpack public key if necessary
        if  self.pkc:
            pk = self.expand_pk(pk)

        x       =   sig[0 : self.n_sz]
        salt    =   sig[self.n_sz : self.n_sz + self.salt_sz]

        #   1:  t <- hash( mu || salt )
        t       =   self.shake256(msg + salt, self.m_sz)

        #   2:  return ( t == [ s^T*P_i*s ] for i in [m] ).
        return  t == self.pubmap(x, pk)


    def open(self, sm, pk):
        """ Verify a signed message  sm = msg + sig. Return msg or None. """
        msg_sz  =   len(sm) - self.sig_sz
        msg     =   sm[:msg_sz]
        sig     =   sm[msg_sz:]
        if not self.verify(sig, msg, pk):
            return None
        return msg

#   === Instantiate UOV Parameter Sets ======================================

uov_1p          =   UOV(gf=256, n=112,  m=44,
                        name='uov-Ip-classic')

uov_1p_pkc      =   UOV(gf=256, n=112,  m=44, pkc=True,
                        name='uov-Ip-pkc')

uov_1p_pkc_skc  =   UOV(gf=256, n=112,  m=44, pkc=True, skc=True,
                        name='uov-Ip-pkc+skc')

uov_1s          =   UOV(gf=16,  n=160,  m=64,
                        name='uov-Is-classic')

uov_1s_pkc      =   UOV(gf=16,  n=160,  m=64, pkc=True,
                        name='uov-Is-pkc')

uov_1s_pkc_skc  =   UOV(gf=16,  n=160,  m=64, pkc=True, skc=True,
                        name='uov-Is-pkc+skc')
uov_3           =   UOV(gf=256, n=184,  m=72,
                        name='uov-III-classic')

uov_3_pkc       =   UOV(gf=256, n=184,  m=72, pkc=True,
                        name='uov-III-pkc')

uov_3_pkc_skc   =   UOV(gf=256, n=184,  m=72, pkc=True, skc=True,
                        name='uov-III-pkc+skc')

uov_5           =   UOV(gf=256, n=244,  m=96,
                        name='uov-V-classic')

uov_5_pkc       =   UOV(gf=256, n=244,  m=96, pkc=True,
                        name='uov-V-pkc')

uov_5_pkc_skc   =   UOV(gf=256, n=244,  m=96, pkc=True, skc=True,
                        name='uov-V-pkc+skc')

#   a list of all variants

uov_all         =   [   uov_1p, uov_1p_pkc, uov_1p_pkc_skc,
                        uov_1s, uov_1s_pkc, uov_1s_pkc_skc,
                        uov_3,  uov_3_pkc,  uov_3_pkc_skc,
                        uov_5,  uov_5_pkc,  uov_5_pkc_skc   ]

