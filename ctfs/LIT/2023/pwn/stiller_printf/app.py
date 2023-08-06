import pwn
from tqdm import tqdm
import secrets

pwn.context.log_level = 'critical'

payload = input("Payload: ").encode('utf-8')
if len(payload) >= 0x100 or not payload.isascii():
    print("NO!")
    exit(1)

def check(payload):
    f = open('secret.txt', 'wb')
    token = secrets.token_hex(0x40).encode()
    f.write(token)
    f.close()
    con = pwn.process("./stiller-printf", stdout=open('/dev/null', 'wb'))
    con.sendline(payload)
    ret = con.poll(True) == 0
    con.close()
    try:
        f = open('win.txt', 'rb')
        ret = f.read() == token and ret
        f.close()
        return ret
    except FileNotFoundError:
        return False


total = 150
passed = sum([check(payload) for _ in tqdm(range(total))])
print(f"Total: {total} Passed: {passed}")
if passed > 58:
    print("CONSISTENT ENOUGH FOR ME :D")
    print("LITCTF{FLAG}")
    exit(0)
print("NOT CONSISTENT ENOUGH")
exit(1)
