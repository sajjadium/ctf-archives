In an ancient tomb, under tons of cob webs, we found this bygone system. It seems to be running SSH, but all we get is "Protocol major versions differ: 2 vs. 1".
Next to it there was a floppy disk containing age-old artifacts.
There were people that could talk to this thing?! Looks like somebody recorded their conversation with the system, as well as the first 512 plain text bytes that were fed into cipher_encrypt() on the client.
Can you find a way to decipher the rest of the conversation?


# Totally Secure Shell
The `ssh-1.0.0.tar` archive contains the source code of SSH version 1.0.0 from 1995. How cool is that?! We found it annoying to build on modern systems, so we attached static builds that should run on modern Linux for your convenience.

Remember, this is a crypto challenge and not reversing. The builds are clean, we did not add backdoors or vulns. Your job is to attack the original implementation of SSH.

As per the challenge description:

> Looks like somebody recorded their conversation with the system, as well as the first 512 plain text bytes that were fed into `cipher_encrypt()` on the client.
>
> Can you find a way to decipher the rest of the conversation?

Good luck & have fun!
