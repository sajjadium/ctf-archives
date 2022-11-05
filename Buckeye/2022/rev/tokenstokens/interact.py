import time
import random
import subprocess
from transformers import AutoTokenizer
import os

tokenizer = AutoTokenizer.from_pretrained("etokenizer")

# tokenize user input
x = input('enter ONE command: ')
tokens = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(x))

args = [os.path.join(os.getcwd(),'tokenstokens')]
for i in range(len(tokens)):
    args.append(str(tokens[i]))

# pretend to do something
for i in range(8): 
    time.sleep(random.randint(1,4))
    print('thinking...')
    if (random.randint(0, 1) == 1):
        print('eek!')
        break

print('running:')

# C program!
popen = subprocess.Popen(args, stdout=subprocess.PIPE)
popen.wait()
print(popen.stdout.read())