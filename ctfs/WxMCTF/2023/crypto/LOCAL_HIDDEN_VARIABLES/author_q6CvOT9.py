import base64
import RC4

flag = "CTF{CENSORED}" # CENSORED
rc4 = RC4.RC4("CENSORED", 0) # CENSORED, established 40-bit key
# the first number may be 8 and the last number may be 9
rc4a = RC4.RC4("CENSORED") # CENSORED, 16-bit pre-shared key

last = rc4.cipher(flag, "plain", "plain")
for i in range(3):
    last = rc4.cipher(last, "plain", "plain")
last = rc4a.cipher(last, "plain", "plain")

print(base64.b64encode(last.encode()))
# b'cMK2wrkTJsOBDsOcwonCumDDiRfDpxcXY0wrwpNMfXvDpWLDh8KycsKpEA=='

