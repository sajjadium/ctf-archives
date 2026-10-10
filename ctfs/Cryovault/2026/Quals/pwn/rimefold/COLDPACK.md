# coldpack -- cold-chain record packer, operator note

coldpack moves fixed-stride record cells through a small staging arena and runs
a self-defragmenting pass over cells you stage.  The handout binary is the 1.3
bench revision of the head; the per-team container runs a later revision.

Connect with `nc <host> <port>`.  Fresh process per connection; nothing you do
on one connection carries to the next.  On connect the head prints a banner
giving its ABI revision and a per-connection id:

    coldpack rimefold abi <rev> ready id=<32 hex>

The handout binary reports `1.3`; your team's live head reports a later
revision.  They share this protocol and arena; confirm anything that matters
against your own head rather than the bench.

## Arena

The arena holds 64 record cells.  Each cell is a fixed 256-byte stride.  Cell
indices are 0..63 and are assigned by the packer when you allocate; you do not
choose a cell's address and no command prints one.

## Protocol (newline-delimited ASCII, hex where noted)

    NEW                       allocate a record cell; prints `OK cell <n>`
    DEL   <cell>              release a cell back to the free list
    STAGE <cell> [<cell>...]  append cells to the staging ring
    FOLD                      dry defragmentation pass over the staging ring;
                              prints `OK folded <k>` and clears the ring
    REAP                      live defragmentation pass; compacts, then runs
                              the packer's reaper; prints `OK reaped <k>`
    DRAW  <cell> <nqwords>    read nqwords (1..32) big-endian qwords from a cell
    PACK  <cell> <qhex>...    write up to 32 qwords into a cell
    STAT                      print slot/live/staged counts
    HELLO                     liveness check
    QUIT

Replies begin `OK` or `ERR <what>` (`arg`, `range`, `state`, `full`, `limit`,
`verb`, `corrupt`).  FOLD and REAP each print one trailing number; FOLD is
non-destructive and clears the ring, REAP compacts for real and then runs the
packer's reaper.

## Limits

    64 cells; 256-byte stride; up to 32 qwords per DRAW/PACK
    5000 commands per connection; 60 s idle timeout

## Syscall filter

The head arms a seccomp filter at start-up.  It is dumped verbatim in
`seccomp.txt`; read it to see what the served process may and may not do.

FLAG FORMAT: an isfcr token with a lowercase [a-z0-9_] body; exact match,
case-sensitive.
