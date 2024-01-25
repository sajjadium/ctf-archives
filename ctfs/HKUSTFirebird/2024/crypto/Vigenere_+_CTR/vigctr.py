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

def ctr(num):
    decimal_num = 0
    power = len(num) - 1
    for digit in num:
        decimal_num += (ord(digit) - ord('A')) * (MOD ** power)
        power -= 1

    decimal_num += 1

    result = ""
    while decimal_num > 0:
        remainder = decimal_num % MOD
        result = chr(remainder + ord('A')) + result
        decimal_num //= MOD

    return(result)

def keygen():
    return(random_block())

def get_iv():
    return(random_block())

def vigenere_ctr_enc(message, key):
    blocks = get_blocks(message)
    nonce = get_iv()
    ctxt = nonce
    for b in blocks:
        to_add = vigenere_enc(nonce, key)
        ctxt += add(b, to_add)
        nonce = ctr(nonce)
    return(ctxt)

def vigenere_ctr_dec(ctxt, key):
    blocks = get_blocks(ctxt)
    nonce = blocks[0]
    ptxt = ""
    for i in range(1, len(blocks)):
        to_add = vigenere_enc(nonce, key)
        ptxt += sub(blocks[i], to_add)
        nonce = ctr(nonce)
    return(ptxt)
        
def read_flag():
    f = open("flag.txt","r")
    flag = f.read()
    f.close()
    return(flag)

if __name__ == "__main__":
    KEY = keygen()
    FLAGTEXT = read_flag()
    CTXT = vigenere_ctr_enc(FLAGTEXT,KEY)
    PTXT = vigenere_ctr_dec(CTXT,KEY)
    assert(PTXT == FLAGTEXT)
    print(CTXT)

# Output : ULDGWMFOXRNTKTVECMMNPQPAJYLJPIXJQUTYRQIQLQSURMZGYUTTPMHOHJAKNQKFFYGTPWXTMFWKHELLZYYFSUDNFKHOZAQIFQDPLUEFFPAILDTXQWWWKIGSVPPTMMWQMODAIBCODZTDSYUQBFSMLSILAZZHVXNTHPUASMZQBBSQZIKHQCLQFQXQAUJGMKACTYBBVMCXUMJOC
# flag is composed of uppercase English characters only without punctuation nor spaces, wrap the flag with 'firebird{...}' before submission