#!/usr/bin/env python3
import asyncio,json,os,random,hashlib

_Q=b'apoorvctf{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}'
_W=13424

def _gn():
    from Crypto.Util.number import getPrime as _f
    return _f(32)

def _ec(k,m):
    from Crypto.Cipher import AES as _C
    from Crypto.Util.Padding import pad as _p
    t=os.urandom(16)
    return t+_C.new(k,_C.MODE_CBC,iv=t).encrypt(_p(m,16))

def _dc(k,c):
    from Crypto.Cipher import AES as _C
    from Crypto.Util.Padding import unpad as _u
    if len(c)<32 or(len(c)-16)%16:return False
    try:_u(_C.new(k,_C.MODE_CBC,iv=c[:16]).decrypt(c[16:]),16);return True
    except ValueError:return False

async def _H(r,w):
    p=_gn();a=random.randint(1,0xFFFF);b=random.randint(1,0xFFFF)
    s=random.randint(0,0xFFFFFFFF);k=os.urandom(32);ct=_ec(k,_Q)
    nc=hashlib.sha256(os.urandom(16)).hexdigest()[:16]
    w.write(json.dumps({"message":"Welcome to the Oracle.",
        "lcg_params":{"A":a,"S_0":s},"flag_ct":ct.hex(),
        "nonce":nc}).encode()+b'\n')
    await w.drain()
    _sq=0

    async def _om(m):
        d=m.get("data")
        if not isinstance(d,int):return({"error":"type"},True)
        return({"status":"success","result":(a*d+b)%p},True)

    async def _ov(m):
        nonlocal _sq,nc;_sq+=1
        t=m.get("token","")
        nc=hashlib.sha256((nc+str(_sq)+str(t)).encode()).hexdigest()[:16]
        return({"status":"ok","seq":_sq,"nonce":nc},True)

    async def _od(m):
        nonlocal s
        cx=m.get("ct","")
        if not isinstance(cx,str):return({"error":"type"},True)
        q=(a*s+b)%p
        try:cb=bytes.fromhex(cx);ci=int.from_bytes(cb,'big')
        except ValueError:return({"error":"hex"},False)
        if ci%p!=q:
            return({"error":"FATAL: Algebraic violation. State desync.",
                     "expected_state":q},False)
        s=q
        return({"status":"math_ok",
                "oracle":"padding_ok" if _dc(k,cb) else "padding_error"},True)

    _D={"math_test":_om,"verify":_ov,"decrypt":_od}

    try:
        while True:
            l=await r.readline()
            if not l:break
            l=l.decode().strip()
            if not l:continue
            try:m=json.loads(l)
            except json.JSONDecodeError:
                w.write(json.dumps({"error":"parse"}).encode()+b'\n')
                await w.drain();break
            fn=_D.get(m.get("option"))
            if fn is None:
                w.write(json.dumps({"error":"unknown"}).encode()+b'\n')
                await w.drain();continue
            rsp,cnt=await fn(m)
            w.write(json.dumps(rsp).encode()+b'\n');await w.drain()
            if not cnt:break
    except Exception:pass
    finally:
        w.close()
        try:await w.wait_closed()
        except Exception:pass

async def _M():
    sv=await asyncio.start_server(_H,'0.0.0.0',_W)
    async with sv:await sv.serve_forever()

if __name__=="__main__":asyncio.run(_M())
