welcome to generic note taking app where you can store all of your notes very securely and not be hacked now with extra risc-v
This is the first of three stages of riscy-stack. Make sure to read the attached README!


# riscy-stack: Userspace

`riscy-stack` consists of a simple userspace application, running on top of a custom kernel, running
on top of patched firmware, all in RISC-V. Each of the three stages is first solved independently of
the other stages for one flag each, then you can chain your exploits to get a bonus flag.

Exploit the userspace binary to gain code execution in userspace. This is the first of three stages.
The userspace blob is embedded into `kernel.bin`, but for your convenience you can also find it in
`userspace.bin`.

DO NOT reverse `kernel.bin` or `firmware.bin`; they are not needed for the first stage and you get
their source code and debug info later (If you think you need it now, which you don't, take it from
the attachments of the other stages).

You only need to know the interface between userspace and the kernel: the kernel loads the userspace
blob at address `0x0800_0000` in one rwx page (page size is 0x1000), starts execution at the
beginning of the blob, and accepts the following syscalls:

| Syscall    | a7     | a0   | a1  | a2   |
| ---------- | ------ | ---- | --- | ---- |
| exit       | 0      | --   | --  | --   |
| read       | 1      | buf  | len | --   |
| write      | 2      | buf  | len | --   |
| map        | 3      | addr | len | prot |
| unmap      | 4      | addr | len | --   |
| print_flag | 0x1337 | --   | --  | --   |

`read` and `write` always transfer the full amount of bytes, e.g. no partial reads. The `addr` and
`len` arguments of `map` and `unmap` have to be multiples of the page size. `prot` can have the
following values: `1: r--, 3: rw-, 4: --x, 5: r-x, 7: rwx`. `print_flag` prints the flag to the
console. Return value is stored in `a0`, positive error code (or 0) in `a1`.
