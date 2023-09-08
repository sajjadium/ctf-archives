Wall Rose

Challenge

nc 34.80.190.155 30001

Instruction

    You have a busybox shell running as user user
    /home/user/rose.ko is a vulnerable kernel driver
    Try exploiting /home/user/rose.ko to achieve privilege escalation
    You may assumed that Busybox, the Linux kernel, and Qemu are not vulnerable.

Files

    ./share/rose.ko: The vulnerable driver
    ./src/rose.c: The source code of rose.c

Flag location

/home/user/flag

Notes

    FG-KASLR is enabled
    Your exploit should be kernel-agnostic. In other words, it should not rely on any kernel offsets


# Wall Rose

## Instruction

- You have a busybox shell running as user `user`
- `/home/user/rose.ko` is a vulnerable kernel driver
- Try exploiting `/home/user/rose.ko` to achieve privilege escalation
- You may assumed that Busybox, the Linux kernel, and Qemu are **not vulnerable**.

## Files

- `./share/rose.ko`: The vulnerable driver
- `./src/rose.c`: The source code of `rose.c`

## Flag location

```
/home/user/flag
```

## Notes

- FG-KASLR is enabled
- **Your exploit should be kernel-agnostic. In other words, it should not rely on any kernel offsets**
