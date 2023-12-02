I here that one line crypto challenges are trending. Try this:

    chall.sage: print((lambda x: (sin(x)*cos(x)).n(1337))(int.from_bytes(open("flag.txt", "rb").read(), "big")))

    NOTE: FLAG is a readable string
