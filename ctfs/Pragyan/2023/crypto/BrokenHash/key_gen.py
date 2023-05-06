from base64 import urlsafe_b64encode
from hashlib import md5
from cryptography.fernet import Fernet

str1: hex = "--REDACTED--"
str2: hex = "--REDACTED--"

hash = md5(bytes.fromhex(str1)).hexdigest()
assert hash == md5(bytes.fromhex(str2)).hexdigest()

key = urlsafe_b64encode(hash.encode())
f = Fernet(key)
