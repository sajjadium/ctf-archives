JuliaPoo
This challenge was so hard to write.
Differential Cryptanalysis Pg 19-29
nc win.the.seetf.sg 3003
Hint:
def get_ddt(sbox):
l = len(sbox)
ddt = np.zeros((l,l), dtype=int)
for i,x in enumerate(sbox):
for j,y in enumerate(sbox):
ddt[i^j][x^y] += 1
return ddt
ddt = get_ddt(SBOX)
ddt_thres = ddt > 4
plt.imshow(ddt_thres)
plt.show()
d = dict([(x,y) for x in range(16) for y in range(16) if ddt_thres[x,y]])
DDT_SBOX = np.array([d[i] for i in range(16)], dtype=np.uint64)
