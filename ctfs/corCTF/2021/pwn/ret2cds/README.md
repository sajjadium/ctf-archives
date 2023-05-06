Pwners keep joking about dropping socat and xinetd 0 days so I rewrote netcat in java. I dare you to pop a shell on me now :^)

https://ret2cds.be.ax/

NOTE: Internet is enabled, please use the provided qemu image, and note that this has been tested to work in a Debian environment for the Docker host. An Ubuntu host is known to have issues with the official solution for the challenge. If you are on Debian, the docker deployment should work for you if you don't want to use the qemu image (but not guaranteed).

QEMU Image: ret2cds-qemu.qcow2.gz

QEMU Example: qemu-system-x86_64 -enable-kvm -serial mon:stdio -hda ret2cds.qcow2 -nographic -smp 1 -m 1G -net user,hostfwd=tcp::1337-:1337 -net nic

QEMU Username: root (no password)
