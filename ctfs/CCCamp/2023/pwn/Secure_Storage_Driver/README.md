Author: Kolja, 0x4d5a
We implemented a driver to securely store our data in kernel space away from prying eyes. What could go wrong?
Some notes about the setup:
For easier exploitation, the driver is exposed via the network. The TCP port 4444 forwards to the harness application that interacts with the driver.
We spawn a new windows machine each time you (re)start the broker. You have 10 minutes to pwn the machine and we will delete it afterwards. Use the IP printed by the broker to throw your exploit.
The server is a Windows Server 2022 Datacenter, 10.0.20348 N/A Build 20348. We provide you the ntoskrnl.exe for this version.
Unless you know what you are doing, we recommend to setup a kernel debugging setup with VirtualBox and NetKD. There are plenty of resources for this around. Enable testsign mode in the debuggee and use OSRLoader to load the driver automatically at system startup.
Due to GCP quotas, we are limited to 12 instances in paralell. If an exception occurs during server spawn, just wait for a few minutes.
