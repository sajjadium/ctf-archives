import secrets

SHIFT = 65
MOD = 26
BLOCKLENGTH = 20

def add(block1,block2):
    assert(len(block1)<= len(block2))
    assert(len(block2)<= BLOCKLENGTH)
    b1upper = block1.upper()
    b2upper = block2.upper()
    b1 = [ ord(b1upper[i])-SHIFT for i in range(len(block1))]
    b2 = [ ord(b2upper[i])-SHIFT for i in range(len(block1))]
    s = [ (b1[i] + b2[i]) % MOD for i in range(len(block1))]
    slist = [ chr(s[i]+SHIFT) for i in range(len(block1))]
    sum = ''.join(slist)
    return(sum)

def sub(block1,block2):
    assert(len(block1)<= len(block2))
    assert(len(block2)<= BLOCKLENGTH)
    b1upper = block1.upper()
    b2upper = block2.upper()
    b1 = [ ord(b1upper[i])-SHIFT for i in range(len(block1))]
    b2 = [ ord(b2upper[i])-SHIFT for i in range(len(block1))]
    s = [ (b1[i] - b2[i]) % MOD for i in range(len(block1))]
    slist = [ chr(s[i]+SHIFT) for i in range(len(block1))]
    sum = ''.join(slist)
    return(sum)

def get_blocks(s):
    blocks = []
    i = 0
    while(i + BLOCKLENGTH<len(s)):
        blocks.append(s[i:i+BLOCKLENGTH])
        i = i + BLOCKLENGTH
    blocks.append(s[i:len(s)])
    return(blocks)

def random_block():
    l = []
    for _ in range (BLOCKLENGTH):
        l.append(chr(secrets.randbelow(MOD)+SHIFT))
    b= ''.join(l)
    return(b)


def vigenere_enc(block,key):
    return(add(block,key))

def vigenere_dec(block,key):
    return(sub(block,key))


def keygen():
    return(random_block())

def get_iv():
    return(random_block())


def vigenere_cbc_enc(message, key):
    blocks = get_blocks(message)
    ctxt = get_iv()
    for b in blocks:
        to_enc = add(b,ctxt[len(ctxt)-BLOCKLENGTH:len(ctxt)])
        ctxt = ctxt + vigenere_enc(to_enc,key)
    return(ctxt)

def vigenere_cbc_dec(ctxt, key):
    blocks = get_blocks(ctxt)
    ptxt = "" 
    for i in range(1,len(blocks)):
        sum = vigenere_dec(blocks[i],key)
        ptxt = ptxt + sub(sum,ctxt[(i-1)*BLOCKLENGTH:(i)*BLOCKLENGTH])
    return(ptxt)



def read_flag():
    f = open("flag.txt","r")
    flag = f.read()
    f.close()
    return(flag)

if __name__ == "__main__":
    KEY = keygen()
    FLAGTEXT = read_flag()
    CTXT = vigenere_cbc_enc(FLAGTEXT,KEY)
    PTXT = vigenere_cbc_dec(CTXT,KEY)
    assert(PTXT == FLAGTEXT)
    print(CTXT)

#Output: AFCNUUOCGIFIDTRSBHAXVHZDRIEZMKTRPSSXIBXCFVVNGRSCZJLZFXBEMYSLUTKWGVVGBJJQDUOXPWOFWUDHYJSMUYMCXLXIWEBGYAGSTYMLPCJEOBPBOYKLRDOJMHQACLHPAENFBLPABTHFPXSQVAFADEZRXYOXQTKUFKMSHTIEWYAVGWWKKQHHBKTMRRAGCDNJOUGBYPOYQQNGLQCITTFCDCDOTDKAXFDBVTLOTXRKFDNAJCRLFJMLQZJSVWQBFPGRAEKAQFUYGXFJAWFHICQODDTLGSOASIWSCPUUHNLAXMNHZOVUJTEIEEJHWPNTZZKXYSMNZOYOVIMUUNXJFHHOVGPDURSONLLUDFAGYGWZNKYXAGUEEEGNMNKTVFYZDIQZPJKXGYUQWFPWYEYFWZKUYUTXSECJWQSTDDVVLIYXEYCZHYEXFOBVQWNHUFHHZBAKHOHQJAKXACNODTQJTGC
#Flag has length 70 and is uppercase english without punctuation nor spaces. Please wrap it in EPFL{...} for submission 
