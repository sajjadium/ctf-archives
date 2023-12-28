Connect to the remote server with `nc -nv challenge09.play.potluckctf.com 31337`. For detailed instructions, see README.md in the provided challenge09-dist.tgz file.


### Setup

Finding and closing all currently open file descriptors on Linux is not easy.
I mean, just look at [this library](https://github.com/cptpcrd/close_fds).
So, I wrote a simple kernel patch that allows you to enumerate currently
open file descriptors from userspace.

I did my best to ensure this patch is memory-safe, so it should definitely
*NOT* introduce any new security vulerabilities such as, say, local privilege
escalation to root.

To prove this, I'm giving you an unprivileged shell on a system with
a secret file (`/flag`) that is only readable by root. If I did my job
properly, you should *NOT* be able to access it.

### How to hack

Install `qemu-system-x86_64` and launch `./run.sh` from the directory with this README.
If your exploit works in this local setup, it should also work on the remote.

You can also run `docker compose up` from the directory with this README to re-create the
exact setup the remote server runs (the server will listen locally on port 31337). This is
basically `run.sh` with TCP connection handling and some proof-of-work slapped on top.

Pro tip: use `base64` to deliver binaries/exploits to the remote.
E.g., on a local machine with Wayland:
```
$ musl-gcc -O2 -static -o pwn pwn.c && base64 pwn | wl-copy
```

On the remote:
```
$ base64 -d >/tmp/pwn <<EOF && chmod +x /tmp/pwn && /tmp/pwn
[...PASTE THE CONTENTS OF YOUR BUFFER HERE...]
EOF
```

### How to hack harder

The challenge environment (kernel/initramfs) used by `run.sh` is located in `prebuilt_system/`.
You can run `docker build --output=prebuilt_system --target=output -f Dockerfile.build_system .`
to (hopefully) re-create the prebuilt files exactly.

For smooth debugging experience, run the following:
```
$ patch -p1 < debugging-goodies.patch
$ docker build --output=custom_system --target=output -f Dockerfile.build_system .
```

This will create an environment suitable for debugging in `custom_system/`:
  * `gdb` will be installed in the guest system for userspace debugging
  * the kernel will be recompiled with various debugging options

The `run.sh` will be modified so that it uses the new environment and awaits
a `gdb` connection from the host before starting the guest. To connect with
`gdb` from the host:
  * cd to `custom_system/`
  * run `tar xf src.tar` to unpack the kernel sources
  * run `gdb vmlinux`
  * type `target remote :1234` and `c` in `gdb`
  * enjoy debugging the kernel with symbols and source code
