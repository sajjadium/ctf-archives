D3v17
During the darkest period of the Molussian freedom movement, two prisioners, like so many of their comrades, had to spend their lives in the dungeons of the Molussian state prison.
Olo, the older prisoner, conveys to Yegussa, the younger, the lessons necessary to perpetuate the struggle for freedom – lessons that he himself once learned from an older prisoner, and which Yegussa is one day to pass on to the next generation.
Embrace the role of Yegussa, don't let the chain be broken, escape from the Molussian Catacomb and become the torchbearer of the fight for freedom.
connect with ssh: ssh the-catacomb@i.be.ax
upload a file to /tmp/exploit: ssh -t the-catacomb@i.be.ax connect $(cat exploit | ssh i.be.ax upload)
CFI is enabled, attack surface is reduced (no io_uring, nft etc.), multiple syscalls are blocked (check nsjail.conf). Too lazy to compile the kernel with clang? Download vmlinux with debug symbols from here. The usage of musl-gcc is recommended.
