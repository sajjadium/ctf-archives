There's an undocumented system call. I wonder if it'll help us?

Scan through kernel memory to find the flag.

There is a new MMIO device we added to Qemu that behaves differently whether you are running in ring 3 or ring 0. It has flags at physical addresses 0x44440000 and 0x55550000. The kernel reads the flag at 0x44440000 at boot and saves it in its memory locally, but not the flag at 0x55550000. So with arbitrary kernel read you can leak the first flag, but to leak the second one you'll need kernel code execution (or do you?)

The flag for this challenge is located at physical address 0x44440000, and a copy is somewhere in the kernel as well (disassemble the kernel!)

Please note: The provided image is slightly different than the Hidden Hard Drive one. This image is used for both parts of the PwnyOS: Zeroday challenge

Note: The kernel is always loaded at a fixed base address.

The qemu patch is provided here if you want to use our qemu mod locally- put fake flags in region4 and region5.

nc zeroday-pwnyos.chal.uiuc.tf 1337

Warning: Booting PwnyOS on real hardware may damage your system. Please read the README.txt file for more info.

Docs (same release notes as hidden hard drive although the kernel here is slightly different- this kernel has the undocumented syscall whereas hidden hard drive doesn't): https://raw.githubusercontent.com/sigpwny/PwnyOS-uiuctf-2021-docs/main/1.1%20Release%20Notes.pdf
