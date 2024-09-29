Secure note-taking app.

You are given a wordlist. Furthermore rockyou.txt may be of use.

Note that the initial data on the server was stored differently, and decryption should take in consideration: nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]. Use pycryptodome and default key derivation hashing algorithm.
