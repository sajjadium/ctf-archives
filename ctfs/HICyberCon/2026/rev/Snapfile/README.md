by Hidden Investigations
Reverse Engineering
A small research-tooling team got tired of shelling out to tar/zip for their dataset snapshots, so they rolled their own compact binary container format, the snapfile (.snap), and a Crystal command-line tool, snaptool, that validates and unpacks them.

The format was never documented outside the team, and the only thing that leaked is the tool itself: a single stripped release binary. No source, no spec, no sample .snap file. If you can hand it a .snap it considers genuine, it will unpack the snapshot's embedded label, which is the flag.

Run it with ./snaptool somefile.snap. It prints the unpacked label on success and invalid snapfile on any failure. There are no other options and no diagnostics. Linux x86-64 ELF, no runtime dependencies beyond a normal glibc system.
