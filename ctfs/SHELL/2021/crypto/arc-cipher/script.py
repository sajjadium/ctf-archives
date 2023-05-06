text = "<flag>"
key = "MANGEKYOU"

s = []

k = []

for i in key:
    k.append(((ord(i))))

for i in range(0,256):
    s.append(i) # i.e. s = [0 1 2 3 4 5 6 7 ..]
    if i >= len(key):
        k.append(k[i%len(key)])

def key_sche(s,k):
    j = 0
    for i in range(0,256):
        j = (j + s[i] + k[i])%256
        temp = s[i]
        s[i] = s[j]
        s[j] = temp
        # print("s in the iteration:",i+1," is :",s)
    return s
def key_stream(text,s):
    ks = []
    i = 0
    j = 0
    status = 1
    while(status == 1):
        i = (i+1) % 256
        j = (j+s[i])%256
        s[i],s[j] = s[j],s[i]
        t = (s[i]+s[j])%256
        ks.append(s[t])
        if len(ks) == len(text):
            status = 0
    return ks

def encrypt(text,k):
    encrypted_txt = ''
    hex_enc_txt = ''
    for i in range(0,len(text)):
        xored = (ord(text[i])) ^ (k[i])
        encrypted_txt +=  chr(xored)
        hex_enc_txt += hex(xored)[2:] + ' '
    li = list(hex_enc_txt)
    li.pop()
    hex_enc_txt = ''.join(li)
    return encrypted_txt,hex_enc_txt

key_new = key_stream(text,key_sche(s,k))
ciphered_txt,ciphered_hex = encrypt(text,key_new)
print("ciphered hex : ",ciphered_hex)
print("ciphered text : ",ciphered_txt)
