You are given ciphertext and leaked keystream states.
Model: S[n+1] = A*S[n] XOR B  over GF(2)
Recover A from consecutive states.
Then decrypt.
