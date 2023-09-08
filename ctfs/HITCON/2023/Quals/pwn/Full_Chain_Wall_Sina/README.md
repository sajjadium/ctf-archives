Wall Sina
Announcement

Hi guys, some people have commented that the src/sina in the wall-sina question is not the same as the sina binary in initramfs, I've updated the attachment, so please re-download the challenge! In addition, we recommend that you use the sina binary in the initramfs to write the exploit. In other words, we recommend that you debug the qemu binary directly (Add the -s flag after qemu-system-x86_64 , then type target remote localhost:1234 in gdb).
Distribution

Challenge

nc 34.80.100.212 30000

Instruction

    You have a chroot busybox shell that contains almost nothing but basic filesystem commands
    /home/user/sina is a vulnerable binary with CAP_SYS_CHROOT capability.
    Try exploiting /home/user/sina to achieve chroot jail break.
    You may assumed that Busybox, the Linux kernel, and Qemu are not vulnerable.

Files

    ./share/sina: The vulnerable binary
    ./src/sina.c: The source code of sina.c
    ./share/libc.so.6: The libc for this challenge
    ./share/ld-linux-x86-64.so.: The linker for this challenge

Flag Location

    /home/user/flag (Outside of the chroot jail)

Note

    Since this is a jail-break challenge, we recommend that you write your exploit in C.
        If you need a sample template, here it is.

Reference

    https://tbhaxor.com/breaking-out-of-chroot-jail-shell-environment/
    https://blog.pentesteracademy.com/privilege-escalation-breaking-out-of-chroot-jail-927a08df5c28


# Wall-Sina

## Instruction

- You have a chroot busybox shell that contains almost nothing but basic filesystem commands
- `/home/user/sina` is a vulnerable binary with `CAP_SYS_CHROOT` capability.
- Try exploiting `/home/user/sina` to achieve chroot jail break.
- You may assumed that Busybox, the Linux kernel, and Qemu are **not vulnerable**.

## Files

- `./share/sina`: The vulnerable binary
- `./src/sina.c`: The source code of `sina.c`
- `./share/libc.so.6`: The libc for this challenge
- `./share/ld-linux-x86-64.so.`: The linker for this challenge

## Flag Location

- `/home/user/flag` (Outside of the chroot jail)

## Note

- **Since this is a jail-break challenge, we recommend that you write your exploit in C.**
    - If you need a sample template, [here](https://gist.github.com/wxrdnx/ea4b97a758b720e39cd8bfb78753c5bb) it is
