Zaza

We pulled this activation stub off a decommissioned "KELPIE" hardware token. It guards the firmware unlock routine behind an activation key. Legend says the key was printed on a sticker that peeled off years ago.

The binary runs a small custom byte-machine over whatever key you type. Feed it the real activation key and it reports "Unlocked"; anything else is "Denied".

$ ./kelpie KELPIE firmware unlock console enter activation key: isfcr{................................}

There is also an undocumented factory self-test that runs the first stage over a fixed test vector — handy for checking your re-implementation of the machine:

$ ./kelpie selftest

The activation key is the flag, in the form isfcr{<32 hex chars>}.

Recover the key. Unlock the firmware.
