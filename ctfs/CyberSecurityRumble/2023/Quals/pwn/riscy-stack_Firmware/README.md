I made OpenSBI even more open by letting you count properties in the FDT, really sensible functionality that's not just there to exercise the parser. In fact now it's so open it might even give you a flag!
This is the third of three stages of riscy-stack, but can be solved independently of the other two. Make sure to read the attached README!


# riscy-stack: Firmware

`riscy-stack` consists of a simple userspace application, running on top of a custom kernel, running
on top of patched firmware, all in RISC-V. Each of the three stages is first solved independently of
the other stages for one flag each, then you can chain your exploits to get a bonus flag.

Exploit the patched OpenSBI firmware to gain code execution in machine mode. This is the third of
three stages, but you can provide code that will be run in kernel space to skip the first and second
stage. You can find the patch in `opensbi.patch`, and an ELF with debug symbols in `firmware.elf`.

The challenge is based on OpenSBI version 1.2, which is commit
`6b5188ca14e59ce7bf71afe4e7d3d557c3d31bf8`. Check out the rest of the source here:
<https://github.com/riscv-software-src/opensbi/tree/6b5188ca14e59ce7bf71afe4e7d3d557c3d31bf8>. Build
the firmware like this:

```sh
git clone https://github.com/riscv-software-src/opensbi.git --branch v1.2 --depth 1
cd opensbi
git apply ../opensbi.patch
make CROSS_COMPILE=riscv64-linux-gnu- PLATFORM=generic
# The firmware is in `build/platform/generic/firmware/fw_dynamic.bin`
```

The patch replaces the "shutdown" call of the legacy extension with a call that can count properties
of nodes in the flattened device tree. Exploit it! The location of the flag in the firmware image is
marked with `CSR{fw_ZZZZZZZZZZZZZZZZ}`, I used a hex editor to insert the flag on the remote, so
otherwise it has the exact same binary.
