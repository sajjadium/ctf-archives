
def new_encryption(file_name, password):
  with open(file_name, "rb") as f:
    plaintext = f.read()
  assert(len(password) == 8)
  assert(b"HiDeteXT" in plaintext)
  add_spice = lambda b: 0xff & ((b << 1) | (b >> 7))
  ciphertext = bytearray(add_spice(c) ^ ord(password[i % len(password)]) for i, c in enumerate(plaintext))
  with open(file_name + "_encrypted", "wb") as f:
    f.write(ciphertext)

def new_decryption(file_name, password):
  with open(file_name + "_encrypted", "rb") as f:
    ciphertext = f.read()
  remove_spice = lambda b: 0xff & ((b >> 1) | (b << 7))
  plaintext = bytearray(remove_spice(c ^ ord(password[i % len(password)])) for i, c in enumerate(ciphertext))
  with open(file_name + "_decrypted", "wb") as f:
    f.write(plaintext)

password = REDACTED

new_encryption("Important", password)
new_decryption("Important", password)
