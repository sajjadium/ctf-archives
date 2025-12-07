boring theme, boring vuln, boring exploit...

can’t stop yawning 🥱

Note 1: If there are many connections, QEMU may slow down, potentially causing the exploit to fail. If it succeeds locally but fails remotely, please open a ticket.

Note 2: If you are using AppArmor, nsjail may not work properly. To disable AppArmor restrictions temporarily, run these commands:

sudo sysctl -w kernel.apparmor_restrict_unprivileged_unconfined=0
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
