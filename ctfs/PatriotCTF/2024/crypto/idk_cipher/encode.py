
import base64
"""
********************************************
*                                          *
*                                          *
********************************************
"""
# WARNING: This is a secret key. Do not expose it.
srt_key = 'secretkey' # // TODO: change the placeholder
usr_input = input("\t:"*10)
if len(usr_input) <= 1:
    raise ValueError("PT must be greater than 1")
if len(usr_input) % 2 != 0:
    raise ValueError("PT can only be an even number")
if not usr_input.isalnum():
    raise ValueError("Only alphabets and numbers supported")
# WARNING: Reversing input might expose sensitive information.
rsv_input = usr_input[::-1]
output_arr = []
for i in range(int(len(usr_input) / 2)):
    c1 = ord(usr_input[i])
    c2 = ord(rsv_input[i])
    enc_p1 = chr(c1 ^ ord(srt_key[i % len(srt_key)]))
    enc_p2 = chr(c2 ^ ord(srt_key[i % len(srt_key)]))
    output_arr.append(enc_p1)
    output_arr.append(enc_p2)
# WARNING: Encoded text should not be decoded without proper authorization.
encoded_val = ''.join(output_arr)
b64_enc_val = base64.b64encode(encoded_val.encode())
R = "R"*20
E = "E"*5
EXCLAMATION = "!"*5
print(f"ULTRA SUPE{R} SECUR{E} Encoded Cipher Text{EXCLAMATION}:", b64_enc_val.decode())
