
print "+===================================+"
print "+    Primality Tester Lite v0.17    +"
print "+===================================+"
print ""

def primtest():
    print "What number would you like to test?"
    num = raw_input()
    try:
        num = long(num)
    except:
        print "invalid number..."
        exit(1)

    print "Enter a false positive probability (empty line for default):"
    prob = raw_input()
    if len(prob) > 0:
        try:
            prob = float(prob)
        except:
            print "invalid number..."
            exit(1)
    else:
        prob = 1e-06

    print "If you would like to enter random byte strings to be used for primality testing, enter the number here (empty line for default PRNG):"
    numrands = raw_input()
    randfunc = None
    if len(numrands) > 0:
        try:
            numrands = long(numrands)
        except:
            print "invalid number..."
            exit(1)
        if numrands > 1024:
            print "That's a bit much don't you think? Upgrade to the PRO version to control more pseudorandomness"
            exit(1)
        print "Enter byte strings hex encoded one line at a time"
        rands = []
        for i in xrange(numrands):
            rand = raw_input()
            try:
                rand = rand.decode('hex')
            except:
                print "invalid hex string..."
                exit(1)
            rands.append(rand)
        def prng(nb):
            if len(rands) == 0:
                return None
            return rands.pop(0)
        randfunc = prng

    print "Ok, all set. Testing for primality..."

    from Crypto.Util.number import isPrime
    try:
        res = isPrime(num, prob, randfunc)
        print "That number is%s prime"%("" if res else "n't")
    except:
        print "Hmmm.... sorry, that's a bad number. Please choose your numbers more carefully."

while True:
    primtest()
    print "Test another number? (y/n):"
    resp = raw_input()
    if len(resp) == 0 or resp[0] == 'n':
        print "Thank you for using our service"
        break
