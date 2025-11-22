Someone didn’t follow proper cryptography hygiene!

You intercepted two signatures from the same service, and it looks like they reused the same ECDSA nonce. The signatures are on different messages, but that repeated nonce might just be your golden ticket.

Your mission: recover the private key from the reused nonce and decrypt the flag.

Tip: ECDSA nonce reuse leaks the private key… if you know how to exploit it.

Challenge author: DJ Strigel
