from Crypto import Random

import aes
import gm

flag = open('flag').read()

key = Random.new().read(16)
pk, sk = gm.generate()

encflag = aes.encrypt(key, flag)
enckey = gm.encrypt(key, pk)

with open('pk', 'w') as f:
	f.write('\n'.join([str(x) for x in pk]))

with open('sk', 'w') as f:
	f.write('\n'.join([str(x) for x in sk]))

with open('key.enc', 'w') as f:
	f.write('\n'.join([str(x) for x in enckey]))

with open('flag.enc', 'w') as f:
	f.write(encflag)