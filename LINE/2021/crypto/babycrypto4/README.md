

Our side-channel attack about ECDSA was quite successful.

We could capture the first 16-bit of the nonces,
which is the first half of them.

Now find out the encryption key.

The victim is using the secp160r1 curve.

The following is the captured data: r, s, k, and hash respectively.

Flag is LINECTF{<encryption key>} and
encryption key is cosists of hex value.
And case is insensitive.

Sorry, curve is secp160r1.

