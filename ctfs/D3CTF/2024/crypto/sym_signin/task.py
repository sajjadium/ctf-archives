import random
from secret import secret_KEY, flag
from task_utils import *

plain = read_from_binary_file('plain')
cipher = []
for i in range(len(plain)):
    x = encrypt(message=plain[i], key=secret_KEY, ROUND=8192)
    cipher.append(x)

write_to_binary_file(cipher, 'cipher')

plain_flag = bytes_to_uint32_list(flag)
enc_flag = []
temp_key = l6shad(secret_KEY)
for i in range(len(plain_flag)):
    enc_flag.append(encrypt(message=plain_flag[i], key=temp_key, ROUND=8192))
    temp_key = l6shad(temp_key)

write_to_binary_file(enc_flag, 'flag.enc')
