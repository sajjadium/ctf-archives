 I heard pwners could utilize an off-by-one error to capture the flag.

nc 34.146.101.4 30007

Hint for beginners:

    First of all, download the attachments and see the source file.
    What you have to do is to guess the flag... No, fake the flag. That means you have to somehow make strncmp(your_try, flag, length) == 0 hold.
    There is little attack surface. Check the spec of suspicious functions.

