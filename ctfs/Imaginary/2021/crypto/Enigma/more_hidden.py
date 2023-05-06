from random import randint

with open('flag.txt', 'r') as f:
  flag = f.read()

out = open('output.txt', 'a')

def caesar_encrypt(flag, key):
  enc_flag = ''
  for i in range(len(flag)):
    if ord(flag[i]) < 65 or ord(flag[i]) > 90:
      enc_flag += flag[i]
    else:
      enc_flag += chr((((ord(flag[i]) - 65) + key[i]) % 26) + 65)
  return(enc_flag)

for i in range(10000): # i wonder why it loops so much
  key = []
  for i in range(len(flag)):
    key.append(randint(1,25)) # ha ha ha, its fully random. you cant decrypt this ;)
  out.write(caesar_encrypt(flag, key) + '\n')
