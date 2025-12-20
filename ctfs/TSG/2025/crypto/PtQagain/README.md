JA /  EN
Author: alcea
I’ll give you p + q encrypted twice with the same scheme! It’s the same thing anyway, so no problem... right?

Hints for beginners:

The result of running problem.py is stored in output.txt.
When you read problem.py, you can see that it encrypts the value FLAG and outputs it. Also, there are some other suspicious data in the output. Since the real value of FLAG is hidden, let's find it out from problem.py and its output!
The original FLAG is a string (more precisely, a byte string), but to encrypt it, it is converted to the corresponding integer m with the code m = bytes_to_long(FLAG). If you get m, then you can obtain the FLAG with the code long_to_bytes(m).
