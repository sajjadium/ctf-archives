import os
import time
import random
from secrets import SECRET_FLAG_TEXT, create_a_perfect_world


CONTESTANTS_PER_SIDE = 20
def generate_contestants():
    ones = []
    zeroes = []
    oprefs = []
    zprefs = []
    while len(ones) < CONTESTANTS_PER_SIDE or len(zeroes) < CONTESTANTS_PER_SIDE:
        contestant = os.urandom(4);
        if contestant[-1] % 2 == 0 and len(zeroes) < CONTESTANTS_PER_SIDE:
            zeroes.append(contestant)
        elif contestant[-1] % 2 == 1 and len(ones) < CONTESTANTS_PER_SIDE:
            ones.append(contestant)

    for i in range(CONTESTANTS_PER_SIDE):
        oprefs.append(random.sample(zeroes, len(zeroes)))
        zprefs.append(random.sample(ones, len(ones)))
    return (ones, zeroes, oprefs, zprefs)



def xor_streams(otp, flag):
    assert len(otp) == len(flag)
    return b"".join([int.to_bytes(x ^ y) for x, y in zip(otp, flag)])




print("""

WELCOME TO MAPLE ISLAND <3
---------------------------------

The name of the game is simple. It's love. They say opposites attract.
You know like North and South, Hot and Cold, etc. The same is said to
be true for parity too, the odd (the ones) and even DWORDS (the zeroes) 
have always had quite steamy and passionate relationships. 
      
Historically speaking, tradition was paramount for this species. The
zeroes scour the world in hopes of find their special One. (Where do
you think the saying comes from? duh.) However, we are in the 21st 
century and must adapt to the new.

So, we made an entire reality TV show about it. The premise is simple:
Screw tradition, in this show, only the Ones are allowed to court the 
zeroes.
 
Stay tuned for the most drama-filled season of Maple Island as of yet
with even more tears, arguments, and passionate moments than ever before.
Will every match made in Maple heaven be stable?
      
Maple Island streaming next month on MapleTV!
      
But wait, lucky viewers have a chance to catch exclusive early-access content
if they can solve the following puzzle below and text the answer to 1-800-MAPLE-1337.
""")

# just for readability on terminal
time.sleep(2)

ones, zeroes, oprefs, zprefs = generate_contestants()
otp = b''
for couple in create_a_perfect_world(ones, zeroes, oprefs, zprefs):
    otp += couple



ctext = xor_streams(otp, SECRET_FLAG_TEXT)
print(f"""
ones: {ones}
zeroes: {zeroes}
oprefs: {oprefs}
zprefs: {zprefs}
ctext: {ctext}
""")





    