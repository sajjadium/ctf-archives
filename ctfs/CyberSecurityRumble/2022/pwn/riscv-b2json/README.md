# Notes for Players

This is a two-staged challenge, with a binary-JSON to JSON converter (`riscv-b2json`) being run by a
RISC-V JIT compiler (`riscv-jit`). Each stage yields a separate flag. In the first stage you have to
exploit the converter, get RISC-V code execution inside the JIT, and execute a dedicated syscall to
get the first flag. In the second stage you have to exploit the JIT, get native code execution, and
read the second flag from the file system. Both exploits are mostly independent; you can work on
them in parallel and combine at the end. But of course you need to solve the first stage before you
can attempt the second stage on the remote server.

Additional clarifications:

## `riscv-b2json`

- The code of `b2json` was produced by clang (except for the three instructions at the entrypoint),
  so there are no weird tricks going on

## `riscv-jit`

- The JIT implements RISC-V faithfully, any mismatch with the spec is accidental

- Comments that specify assembly snippets are accurate, you do not need to disassemble the code
  snippets to check all of them

- The `vm_verbose` flag is included so you can use the same `riscv-jit` binary for local debugging;
  if you think about enabling `vm_verbose` using a memory corruption: The intended solution does not
  do that

- Please note that the `read` and `write` ecalls may read/write partially; if your exploit works
  locally but fails on the remote server, this might be the reason. In that case, reduce your
  payload size or issue multiple small (less than 1 KiB) reads/writes
