from Cryptodome.Util.number import*

e = 0x10001
s = pow(p + q, 2)
n = p*q
a = pow(s, 3, r)
b = (s - q*(2*p + q))*r

m_list = [findme]

c_list = []
for i in range(len(m_list)):
    m = bytes_to_long(m_list[i])
    c = pow(m*r, e, n)

    c_list.append(c)

output = open("output.txt", "w")
output.writelines([str(i) + "\n" for i in [e, s, n, a, b, c_list]])
output.close()
