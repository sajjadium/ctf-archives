import hashlib
import subprocess

def md5sum(b: bytes):
    return hashlib.md5(b).digest()[:3]


whitelisted_cmd = b'echo lmao'
whitelisted_hash = md5sum(whitelisted_cmd)

def main():
    while True:
        cmd = input('> ').encode()
        if cmd == b'exit':
            print('Goodbye')
            exit()

        if md5sum(cmd) != whitelisted_hash:
            print(f'Invalid command, try "{whitelisted_cmd.decode()}"')
            continue

        try:
            out = subprocess.check_output(['/bin/bash', '-c', cmd])
            print(out.decode())
        except subprocess.CalledProcessError as e:
            print(f'Command returned non-zero exit status {e.returncode}')

if __name__ == "__main__":
    main()
