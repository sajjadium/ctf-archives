Author: settyan117

    On December 14, 2024, a secret key p, q of RSA was found in a scattered state. The victim seems to have encrypted some message by themselves. As a detective, I want you to decipher the message left by the victim.

Hints for beginners:

    The result of running challenge.py is stored in output.txt.
    When you read challenge.py, you can see that it encrypts the value flag and outputs it. Also, there are some other suspicious data in the output. Since the real value of flag is hidden, let's find it out from challenge.py and its output!
    The original flag is a string (more precisely, a byte string), but to encrypt it, it is converted to the corresponding integer m with the code m = int.from_bytes(flag, 'big'). If you get m, then you can obtain the flag with the code m.to_bytes((m.bit_length()-1)//8 + 1, 'big').
