FizzBuzz101
A hardware quirk, a micro-architecture attack, and a kernel exploit all in one!
Note that the remote environment is on a Cascade Lake generation processor on a dedicated AWS instance. KPTI is disabled in the distributed run script, as KPTI is automatically disabled on remote since the kernel detects the relevant hardware mitigations KPTI was designed against. An AMD CPU will NOT work for this challenge.
connect with ssh: ssh sysruption@i.be.ax
upload a file to /tmp/exploit: ssh -t sysruption@i.be.ax connect $(cat exploit | ssh i.be.ax upload)
To help with debugging the hardware quirk and micro-architecture attack, we have provided special instances below for debugging purposes. These just boot up into a root shell with the flag removed, with no differences otherwise - it runs on the same hardware.
connect for debugging with ssh: ssh sysruption-backdoor@i.be.ax
upload for debugging: ssh -t sysruption-backdoor@i.be.ax connect $(cat exploit | ssh i.be.ax upload)
For those interested in building the kernel from scratch, feel free to download it from https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.3.4.tar.xz
