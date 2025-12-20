JA /  EN
Author: settyan117
My original ultra mega super-duper ultimate strongest exponent!

Hints for beginners:

The result of running problem.py is stored in output.txt.
When you read problem.py, you can see that it encrypts the value flag and outputs it. Since the real value of flag is hidden, let's find it out from problem.py and its output!
The original flag is a string, but to encrypt it, it is converted to the corresponding integer m with the code m = int.from_bytes(flag, 'big'). If you get m, then you can obtain the flag with the code m.to_bytes((m.bit_length()-1)//8 + 1, 'big').
