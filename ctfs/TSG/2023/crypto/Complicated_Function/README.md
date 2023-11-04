JA / EN

    You should not use simple function like f(p) = p + 8 to get q. It surely becomes secure if f(p) is complicated!

Hints for beginners:

    The result of running challenge.py is stored in output.txt.
    If you read challenge.py, you will see that it reads the flag from secrets.py, encrypts it, and outputs it. As secret.py is not included in distributed files, read challenge.py carefully and find the vulnerability!
    The original flag is a string (more precisely, a byte string), but to encrypt it, it is converted to the corresponding integer m with the code m = int.from_bytes(flag, 'big'). If you get m, then you can obtain the flag with the code m.to_bytes((m.bit_length()-1)//8 + 1, 'big').
