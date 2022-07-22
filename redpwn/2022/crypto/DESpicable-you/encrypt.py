from os import urandom

def encipher(a,b):
    c = ''
    for i, j in zip(a,b):
        c+=chr(ord(i)^ord(j))
    return c

def rekey(key):
    k = ""
    for i,c in enumerate(key):
        if i == len(key)-1:
            k += c
            k += chr(ord(c)^ord(key[0]))
        else:
            k += c
            k += chr(ord(c)^ord(key[i+1]))
    key = k

def main():
    key = urandom(8)

    with open('flag.txt') as f:
        plaintext = f.read()

    i = 0
    ct = ''
    while i < len(plaintext):
        ct += encipher(plaintext[i:i+len(key)],key)
        i += len(key)
        rekey(key)
    f2 = open('output.txt', 'w')
    f2.write(ct)
    f2.close()

main()

