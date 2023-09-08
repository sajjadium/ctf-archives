Wall Maria

Challenge

nc 35.221.156.78 30002

Instruction

    You have a busybox shell running as root
    The Qemu running this VM is built with a custom, vulnerable PCI device called maria
    Try exploiting the maria PCI device to achieve Qemu escape
    You may assumed that Busybox, the Linux kernel, and other parts of Qemu are not vulnerable.

Files

    ./share/qemu-system-x86_64: The vulnerable Qemu binary
    ./src/maria.c: The source code of the custom PCI device

Flag location

    /home/user/flag (The flag is located outside the virtual machine)

Notes

    Your exploit should be library-agnostic. In other words, it should not rely on shared library offsets.


# Wall Maria

## Instruction

- You have a busybox shell running as root
- The Qemu running this VM is built with a custom, vulnerable PCI device called `maria`
- Try exploiting the `maria` PCI device to achieve Qemu escape
- You may assumed that Busybox, the Linux kernel, and other parts of Qemu are **not vulnerable**.

## Files

- `./share/qemu-system-x86_64`: The vulnerable Qemu binary
- `./src/maria.c`: The source code of the custom PCI device

## Flag location

- `/home/user/flag` (The flag is located outside the virtual machine)

## Notes

- **Your exploit should be library-agnostic. In other words, it should not rely on shared library offsets.**
