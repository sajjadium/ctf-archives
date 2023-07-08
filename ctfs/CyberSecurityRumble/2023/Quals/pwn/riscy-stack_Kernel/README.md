I hear Rust is so secure and RISC-V is gonna be the next big architecture, so of course I have the best of both in my new kernel.
This is the second of three stages of riscy-stack, but can be solved independently of the first one. Make sure to read the attached README!


# riscy-stack: Kernel

`riscy-stack` consists of a simple userspace application, running on top of a custom kernel, running
on top of patched firmware, all in RISC-V. Each of the three stages is first solved independently of
the other stages for one flag each, then you can chain your exploits to get a bonus flag.

Exploit the custom kernel to gain code execution in kernel space. This is the second of three
stages, but you can provide code that will be run in userspace to skip the first stage. You can find
the source code of the kernel in `kernel_src.zip`, and an ELF with debug symbols in
`kernel_newuser.elf`. Build the kernel like this:

```sh
cd kernel_src
cd kernel
cargo build --release --features replace-userspace
riscv64-linux-gnu-objcopy -O binary ../target/riscv64gc-unknown-none-elf/release/kernel kernel_newuser.bin
```

DO NOT reverse `firmware.bin`; it is not needed for the second stage and you get its source code and
debug info later (If you think you need it now, which you don't, take it from the attachments of the
other stages).

When looking at the kernel code, keep in mind that only the code that's reachable from userspace is
relevant. For example you might want to look at trap handling, the syscall interface, memory
management, ..., and skim over stuff like the precise boot process where the kernel is relocating
itself two times. The location of the flag in the kernel image is marked with
`CSR{kern_YYYYYYYYYYYYYY}`, I used a hex editor to insert the flag on the remote, so otherwise it
has the exact same binary.
