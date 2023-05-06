Description:

We discovered that the ButcherCorp has a data center in the city of
Boston. Each server of this data center has a custom BMC (Baseboard Management
Controller), named 'Butcher BMC' and they manage the servers remotely through an
exposed IPMI interface. Luckly, the Rebelious Fingers were able to deploy a
backdoor on this data center. Below is the information that they sent to us:

root@butcher:~# journalctl -b --no-pager | grep Echo
May 25 00:45:49 butcher ipmid[234]: Registering OEM:[0X003039], Cmd:[0X7E] for Echo Commands

Instructions:

1- Install dependency, e.g.,:
$ sudo apt install ipmitool

2- Connect to server, e.g.,:
$ nc butcherbmc.pwn2.win 1337

3- Solve PoW, get your ipmi port, and wait for system initialization.

4- Use ipmitool to run commands, e.g.,:
$ ipmitool -I lanplus -H butcherbmc.pwn2.win -p <ipmi port> -U root -P 0penBmc chassis status

Note that the credentials are the default (i.e., root:0penBmc).
