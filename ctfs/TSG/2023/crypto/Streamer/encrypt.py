import secrets
import hashlib
import base64
import re

pattern = re.compile("[a-zA-Z0-9!-/:-?\[-`|~]+")
flag_content = b"@@REDUCTED@@"
assert pattern.fullmatch(flag_content.decode())

flag_hash = hashlib.md5(flag_content).digest()
flag = b"TSGCTF{"+flag_content+b"@"+base64.b64encode(flag_hash)+b"}"

key_stream = list(secrets.token_bytes(16))
encrypted_flags = [flag[i]^key_stream[i%16] for i in range(len(flag))]

print("cipher =",encrypted_flags)
print("flag_length =",len(flag))