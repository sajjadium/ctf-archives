
from Crypto.Util.number import getPrime, bytes_to_long, GCD
from random import randint


flag = bytes_to_long(b"#REDACTED")
p = getPrime(1024)
q = getPrime(1024)
N= p*q
e = 0x10001
x = 20525505347673424633540552541653983694845618896895730522108032420068957585904662258035635517965886817710455542800215902662848701181206871835128952191014493697284969437314225749429743933083828160659364661388058087193251081260335982254080118777967019114025487327203682649658969427745709426290533798413074002576442578240125282339739757429305467392467056855474421076815986701014649799010560681947651299817835748393824150668018627770878313651343270246832490595870418506765783183714239947943610319258616554427446129948999323762841507343205007649094350172991183628556644081749900113654945488511477133416252720845890086594005
c = pow(flag, e , N)
enc_pq = []
bin_p = bin(p)[2:]
bin_q = bin(q)[2:]

for i in range(512):
        while True:
            r = randint(1, N)
            if GCD(r, N) == 1:
                bin_r = bin(r)[2:]
                p_bit = (pow(x, int(bin_r + bin_p[i], 2), N) * r ** 2) % N

                enc_pq.append(p_bit)
                break
for i in range(512):
        while True:
            r = randint(1, N)
            if GCD(r, N) == 1:
                bin_r = bin(r)[2:]
                q_bit = (pow(x, int(bin_r + bin_q[512+i], 2), N) * r ** 2) % N
                enc_pq.append(q_bit)
                break

f = open("Output.txt", "w")
f.write(f"{N = }\n")
f.write(f"{e = }\n")
f.write(f"{c = }\n")
f.write(f"{x = }\n")
f.write(f"{enc_pq = }\n")
f.close()