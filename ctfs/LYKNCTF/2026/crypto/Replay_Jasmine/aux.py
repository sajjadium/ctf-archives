import hashlib
import hmac as _hm
import os
import struct

def _hk(ik,sl,fo,ln):
    pk=_hm.new(sl,ik,hashlib.sha512).digest()
    ok=b"";T=b""
    for i in range(1,(ln+63)//64+2):
        T=_hm.new(pk,T+fo+bytes([i]),hashlib.sha512).digest()
        ok+=T
        if len(ok)>=ln:break
    return ok[:ln]

def _sk(k32,ch,ct):
    h=hashlib.sha512()
    h.update(k32);h.update(ch);h.update(struct.pack("<Q",ct))
    return h.digest()

def _xb(a,b):
    return bytes(x^y for x,y in zip(a,b))

def _ig(bk,ch,k32,ct):
    return _xb(_xb(bk,_sk(k32,ch,ct)),ch)

def _sp(dt,bs=64):
    return[dt[i:i+bs] for i in range(0,len(dt),bs)]

def _fe(bl,k32,iv):
    ch=iv;ou=[]
    for i,b in enumerate(bl):
        c=_ig(b,ch,k32,i);ch=c;ou.append(c)
    return ou

def _fd(bl,k32,iv):
    ch=iv;ou=[]
    for i,b in enumerate(bl):
        p=_ig(b,ch,k32,i);ch=b;ou.append(p)
    return ou

def _be(bl,k32,iv):
    n=len(bl);rs=list(bl);ch=iv
    for i in range(n-1,-1,-1):
        c=_ig(rs[i],ch,k32,n-1-i);ch=c;rs[i]=c
    return rs

def _bd(bl,k32,iv):
    n=len(bl);rs=list(bl);ch=iv
    for i in range(n-1,-1,-1):
        p=_ig(rs[i],ch,k32,n-1-i);ch=rs[i];rs[i]=p
    return rs

def _pd(dt,bs=64):
    p=bs-(len(dt)%bs)
    return dt+bytes([p]*p)

def _up(dt,bs=64):
    p=dt[-1]
    if p==0 or p>bs or dt[-p:]!=bytes([p]*p):raise ValueError("invalid padding")
    return dt[:-p]

class Shiina256PIGE:
    def __init__(self,mk):
        if len(mk)!=32:raise ValueError("master_key must be 32 bytes")
        self._mk=mk
    def _kd(self,nc):
        mk=self._mk
        en=_hk(mk,nc,b"shiina256pige-enc-v1",32)
        mc=_hk(mk,nc,b"shiina256pige-mac-v1",32)
        fv=_hk(mk,nc,b"shiina256pige-ivfwd-v1",64)
        bv=_hk(mk,nc,b"shiina256pige-ivbwd-v1",64)
        return en,mc,fv,bv
    def _mi(self,nc,ad,ct):
        return nc+struct.pack("<Q",len(ad))+ad+struct.pack("<Q",len(ct))+ct
    def encrypt(self,pt,ad=b""):
        nc=os.urandom(96)
        en,mc,fv,bv=self._kd(nc)
        bl=_sp(_pd(pt))
        bl=_fe(bl,en,fv)
        bl=_be(bl,en,bv)
        ct=b"".join(bl)
        tg=_hm.new(mc,self._mi(nc,ad,ct),hashlib.sha512).digest()
        return nc+ct+tg
    def decrypt(self,da,ad=b""):
        if len(da)<96+64+64:raise ValueError("ciphertext too short")
        nc,ct,tg=da[:96],da[96:-64],da[-64:]
        if len(ct)==0 or len(ct)%64:raise ValueError("invalid ciphertext length")
        en,mc,fv,bv=self._kd(nc)
        ex=_hm.new(mc,self._mi(nc,ad,ct),hashlib.sha512).digest()
        if not _hm.compare_digest(tg,ex):raise ValueError("authentication failed")
        bl=_sp(ct)
        bl=_bd(bl,en,bv)
        bl=_fd(bl,en,fv)
        return _up(b"".join(bl))
