exec('def f(x):'+'yield((x:=-~x)*x+-~-x)%727;'*100)
g=f(id(f));print(*map(lambda c:ord(c)^next(g),list(open('f').read())))