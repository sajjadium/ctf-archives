Someone’s been messing with your secure communication channel… and they’ve left traces!

You’ve intercepted a mysterious ciphertext and a series of leaked internal states from a rogue pseudorandom generator. It seems the generator is powered by a secret 32×32 matrix A and an unknown 32-bit vector B.

Your mission: reverse-engineer the system! Use the leaked states to reconstruct the hidden matrix, uncover the XOR constant, and decrypt the message. Only then will the true flag reveal itself.

Remember: the keystream bytes come from the lowest byte of each internal state. Pay attention to the details.

Challenge author: DJ Strigel
