qemu-system-riscv64 -machine virt -bios none -kernel main.elf -m 3M -nographic -serial mon:stdio
# I personally tested on QEMU version 10.0.0 on Debian, but should work on any recent version of qemu