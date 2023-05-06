import secrets

flag = b'flag{******************************************************}'
key = secrets.token_bytes(len(flag))

with open('task.txt', 'w') as f:
    f.write(''.join(f'{((flag[i] + key[i]) % 256):02x}' for i in range(len(flag))) + '\n')
    shift_flag = flag[-6:] + flag[:-6]
    f.write(''.join(f'{((shift_flag[i] + key[i]) % 256):02x}' for i in range(len(flag))) + '\n')
