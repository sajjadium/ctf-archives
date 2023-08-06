#/usr/bin/python3
# nowadays, setattr jails seem to be all the hype, and everyone loves builtins, so enjoy a setattr jail with builtins :>
for _ in range(2):
    src = input("Src: ")
    dst = input("Dst: ")
    assert "." not in src and dst.count(".") < 3
    for x in dst.split("."):
        assert x not in ["setattr", "getattr", "print"], "Hey im using those!" 
    a = "." in dst
    b = dst.split(".")
    x = dst
    pdist = __builtins__
    dst = getattr(__builtins__, dst.split(".")[0])
    if a:
        for x in b[1:]:
            pdist = dst
            dst = getattr(dst, x)
    src = getattr(__builtins__, src)
    setattr(pdist, x, src)

print(__builtins__)