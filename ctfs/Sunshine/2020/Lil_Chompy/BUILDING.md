Easiest way to get up and running is just:

`docker run -p 20003:20003 -itd kjcolley7/lilchompys-redacted:release`

There's also the `debug` tag which swaps out `lilchompys` with a version of it
built with `CHOMPY_DEBUG=1` (in the archive as `lilchompys.debug`):

`docker run -p 20003:20003 -itd kjcolley7/lilchompys-redacted:debug`


Instructions for SunshineCTF 2020 players to build and deploy locally:

1. `git clone https://github.com/C0deH4cker/PwnableHarness.git`
2. `mkdir PwnableHarness/LilChompys`
3. Copy contents of lilchompys.tar.gz into PwnableHarness/LilChompys
4. `cd PwnableHarness`
5. Build and start Docker container locally: `make docker-start`
6. Connect to locally running server: `nc localhost 20003`

In the PwnableHarness/LilChompys directory, the binaries `lilchompys`,
`lilchompys.debug`, and `libcageheap.so` will all be built from the sources.
Be sure to save copies of the original ones before making any changes to the
code or build settings!

You can run the challenge locally without the TCP server and Docker by just
running `./lilchompys` (or `./lilchompys.debug`). This is better for debugging,
though be aware that it will be running in a different environment than the
real challenge.
