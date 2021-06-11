import string, random, os, sys

pool = string.ascii_letters + string.digits
random.seed(open('/dev/random', 'rb').read(16))

flag_parts = ['F', 'f', 'L', 'l', 'A', 'a', 'G', 'g', '70', '102', '76', '108',
        '65', '97', '71', '103', '0x46', '0x66', '0x4c', '0x6c', '0x41', '0x61',
        '0x47', '0x67', 'fl', 'la', 'ag', 'fla', 'lag', 'flag', 'FLAG', 'FLA',
        'LAG', 'FL', 'LA', 'AG']

def randint(x):
    return random.randint(0, x - 1)

def randstr():
    msg = ''
    for i in range(25):
        msg += pool[randint(len(pool))]
    return msg

def main():
    if len(sys.argv) != 2:
        print('Usage: {} FLAG_VALUE'.format(sys.argv[0]))
        exit(1)

    flag = open(sys.argv[1], 'r').read().strip()

    def flatten(aval, bval, cval):
        return aval * 50 + bval * 5 + cval

    base = 'flag_dir'
    os.mkdir(base)
    
    flagpos = randint(len(flag_parts) * 50)
    for a in range(len(flag_parts)):
        aa = base + '/' + flag_parts[a]
        os.mkdir(aa)
        for b in range(10):
            bb = aa + '/' + randstr()
            os.mkdir(bb)
            for c in range(5):
                cc = bb + '/' + randstr()
                with open(cc, 'w') as f:
                    if flatten(a, b, c) == flagpos:
                        print('Flag is located at: ./' + cc)
                        f.write(flag + '\n')
                    else:
                        f.write(randstr() + '\n')

if __name__ == '__main__':
    main()
