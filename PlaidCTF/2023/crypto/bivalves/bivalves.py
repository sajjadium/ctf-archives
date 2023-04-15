from bitstream import BitStream
from bitstring import BitArray
import os

KEY = BitArray(os.urandom(10)).bin
IV = BitArray(os.urandom(10)).bin

print(IV)

state = BitArray(bin=(KEY + '0101000001010' + IV + '0'*4))
output_stream = BitStream()

def step(out=True):
    if out:
        output_stream.write(state[65] ^ state[92], bool)
    t1 = state[65] ^ state[92] ^ (state[90] & state[91]) ^ state[170]
    t2 = state[161] ^ state[176] ^ (state[174] & state[175]) ^ state[68]
    for i in range(92, 0, -1):
        state.set(state[i - 1], i)
    state.set(t2, 0)
    for i in range(176, 93, -1):
        state.set(state[i - 1], i)
    state.set(t1, 93)

for _ in range(708):
    step(False)

pt=BitArray(bytes=('''There once was a ship that put to sea
The name of the ship was the Billy O' Tea
The winds blew up, her bow dipped down
Oh blow, my bully boys, blow (huh)

Soon may the Wellerman come
To bring us sugar and tea and rum
One day, when the tonguing is done
We'll take our leave and go

She'd not been two weeks from shore
When down on her right a whale bore
The captain called all hands and swore
He'd take that whale in tow (huh)

Soon may the Wellerman come
To bring us sugar and tea and rum
One day, when the tonguing is done
We'll take our leave and go

- '''.encode('utf-8') + (open('flag.txt', 'rb').read())))

ciphertext = BitStream()
for i in range(len(pt)):
    step()
    ciphertext.write(output_stream.read(bool, 1)[0] ^ pt[i], bool)

print(ciphertext.read(bytes, len(pt) // 8))
