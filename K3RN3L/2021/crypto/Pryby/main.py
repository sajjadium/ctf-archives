from Crypto.Util.number import bytes_to_long 
def f(n):
    q=[True]*(n + 1)
    r=2
    while r**2<=n:
        if q[r]:
            for i in range(r**2,n+1,r):q[i] = False
        r += 1
    return [p for p in range(2,n+1) if q[p]]
class G:
    def __init__(self, f):
        self.f = f
        self.state = 1
    def move(self):
        q=1
        for p in self.f:
            if self.state%p!=0:
                self.state=self.state*p//q
                return
            q*=p
flag = open('flag.txt','r').read().strip().encode()
flag=bytes_to_long(flag)
gen = G(f(pow(10,6)))
for _ in range(flag):gen.move()
print('enc =',gen.state)
# enc = 31101348141812078335833805605789286074261282187811930228543150731391596197753398457711668323158766354340973336627910072170464704090430596544129356812212375629361633100544710283538309695623654512578122336072914796577236081667423970014267246553110800667267853616970529812738203125516169205531952973978205310