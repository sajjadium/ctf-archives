import random
import time
from secret import flag

def get_random_array(x): 
    y = list(range(1,x))
    random.Random().shuffle(y)
    return y

my_seed = bytes(get_random_array(42))
random.seed(my_seed)
my_random_val = random.getrandbits(9999)
print(f"my seed: {my_seed.hex()}")

start = time.time()
ur_seed = bytes.fromhex(input("Enter your seed! > "))
if ur_seed == my_seed:
    print("Hey that's my seed! No copying >:(")
    exit()
if time.time() - start > 5:
    print("Too slow I've already lost interest in seeds -_- ")
    exit()

random.seed(ur_seed)
ur_random_val = random.getrandbits(9999)

print(flag) if my_random_val == ur_random_val else print("in rand we trust.")