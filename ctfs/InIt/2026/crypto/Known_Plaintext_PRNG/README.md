OffScript

A custom stream-like cipher encrypts a flag in four-byte blocks. Each block is XORed with a 32-bit key, and the key is mutated using a predictable linear congruential generator. The starting key was supposed to be secret, but the flag format reveals the first plaintext block.
