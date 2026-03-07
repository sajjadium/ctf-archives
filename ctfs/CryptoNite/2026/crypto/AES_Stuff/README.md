We built a “secure” encryption service using Advanced Encryption Standard. To keep things simple, it runs in Electronic Codebook mode. The service works like this: -You send arbitrary plaintext. -The server appends a secret flag to your input. -The combined message is padded and encrypted. -The ciphertext is returned to you as hex. -The encryption key is fixed and unknown to you.

You may query the oracle as many times as you like. Can you recover the secret flag?

Link: https://aes-challenge-thingy.vercel.app/api/oracle
