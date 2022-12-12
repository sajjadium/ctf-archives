from Crypto.Util.number import *

with open('flag.txt', 'rb') as f:
    msg = f.read()

junk_msg = [os.urandom(120) for i in range(65536)]
for i in range(len(msg)):
    junk_msg[i] = junk_msg[i][:i] + bytes([msg[i]]) + junk_msg[i][i+1:]

p = 990367536408524906540912485167816012092796554403092639917950993714265910699138052663068131070259292593771612112016905904144038137551264432483487958987773403759866096258076571660618998739176702013853258687325567753038298889168254166361474202422033630403618955865472205722190830457928271527937
g = 745013838642250986737914025336862504661062017981819269513542907265222774830330586097756124678061002877695509685688964126565784246358161149675046363463274308162223776270434432888284419417479549219965033745142547821863438374478028783067286583042510995247992045551680383288951502770625897136683

Zp = Zmod(p)
g = Zp(g)
junk_msg = [Zp(bytes_to_long(msg)) for msg in junk_msg] 
junk_cipher = []

for i in range(65536):
    junk_cipher.append(ZZ(sum(junk_msg[j] * g^(i*j) for j in range(65536))))

def generate_params(beta):
    n = 1024
    delta = 0.642

    p_upper_bound = 1 << (n // 2)
    p_lower_bound = p_upper_bound >> 1
    p = random_prime(p_upper_bound, lbound=p_lower_bound)
    pqdiff_upper_bound = 1 << int(n * beta)
    '''
    Jinx: QUADRA KILL
    '''
    pqdiff_lower_bound = pqdiff_upper_bound * 0.7777777
    q = next_prime(p + random_prime(pqdiff_upper_bound, lbound=pqdiff_lower_bound))
    N = p * q
    AAHPH = (p^2 - 1) * (q^2 - 1)

    d_upper_bound = 1 << (int(n * delta))
    d_lower_bound = d_upper_bound >> 1
    while True:
        d = random_prime(d_upper_bound, lbound=d_lower_bound)
        if gcd(d, AAHPH) == 1:
            e = inverse_mod(d, AAHPH)
            if gcd(e, AAHPH) == 1:
                break
    return (N, e), (N, e, d, p, q)

'''
EDG.Clearlove
'''
beta = 0.4396

pk, sk = generate_params(beta)
N, e, d, p, q = sk
print('PLEASE WAIT...')
ZN = Zmod(N)
garbage_cipher = [ZN(jc) ^ e for jc in junk_cipher]

N, e = pk
troll = list(map(str, garbage_cipher)) + ['-' * 77, f'{N = }', f'{e = }']

e, d, g = 'Clearlove', 'LeeSin', '4396'
EDG = '\n'.join(troll)
with open('output.txt', 'w') as f:
    f.write(EDG)