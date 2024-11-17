from Crypto.Util.number import *
from Secret import flag2

def leak_info(primes):
    mod=getPrime(4096)
    parameters=[getPrime(4096) for _ in range(3)]
    cnt=0
    for i in range(3):
        cnt+=primes[i]*parameters[i]
        cnt%=mod
    print(f"---leak info---\n{cnt=}\n{parameters=}\n{mod=}")

primes=[getPrime(512) for _ in range(3)]
p, q, r=primes[0], primes[1], primes[2]
n=p*q*r
e=0x10001
c=pow(bytes_to_long(flag2), e, n)
print(f"{n=}\n{e=}\n{c=}")
leak_info(primes)

'''
     ("`-/")_.-'"``-._
      . . `; -._    )-;-,_`)
     (v_,)'  _  )`-.\  ``-'
    _.- _..-_/ / ((.'
  ((,.-'   ((,/             
'''
