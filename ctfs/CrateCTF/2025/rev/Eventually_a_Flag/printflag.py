import string, time

alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!#$%&()*+,-./:;<=>?@[]^_{|}~åäö "

ciphertext = "cq rbäl{%$0eYXm&5bV( Z&j@|2VoT2fVzö5)äXMömlfpmhhtawc]eiwvl2ö26a4Vm$3bP6@Rm5#r)ToR2p!XlZ.B8@);äfkldq=<}{[:#RkY4h55m8!r(,E{g:#z)-yRRäAs#nH?rbi|$|"

# TODO: Too much recursion?
def fibonacci(n: int) -> int:
    return n if n < 2 else fibonacci(n - 2) + fibonacci(n - 1)

for i, c in enumerate(ciphertext):
    print(alphabet[(alphabet.index(c) + fibonacci(i)) % len(alphabet)], end="", flush=True)
    time.sleep(0.03)
print()
