from secret import flag
import os
import random

state_len = 624*4
right_pad = random.randint(0,state_len-len(flag))
left_pad = state_len-len(flag)-right_pad
state_bytes = os.urandom(left_pad)+flag+os.urandom(right_pad)
state = tuple( int.from_bytes(state_bytes[i:i+4],'big') for i in range(0,state_len,4) )
random.setstate((3,state+(624,),None))
outputs = [random.getrandbits(32) for i in range(624)]
print(*outputs,sep='\n')


