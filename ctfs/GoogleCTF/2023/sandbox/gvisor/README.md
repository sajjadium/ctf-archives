gVisor is a container sandbox with a kernel written in the memory safe language Go.
However, using unsafe pointers erroneously could still make it unsafe.
The gVisor `runsc` in this challenge is patched on the commit version `192bfb03fb2f8f869d834885716a1b904f5c930d`.
Read `Makefile` to learn how the `challenge` is built.
