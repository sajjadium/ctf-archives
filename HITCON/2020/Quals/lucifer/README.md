Lucifer challenge
-


## Goal

+ Read the flag in `C:\flag.txt` (readable only by SYSTEM)


## Environment

+ Windows 10 Pro 20h2
	+ Verion 10.0.19042.630
+ Load lucifer.sys (sha1: b086d6d477dbebe9594b1924ee315965963ff83c)
+ Account (Remote are different)
	+ ctf/hitcon2020
	+ user/hitcon2020
+ ntoskrnl.exe (sha1: 0aca917d44c6f5eee7abcb2aa1edb64afa00dad8)

### Test

+ You can use follow command and use vnc for testing :

```
/usr/bin/qemu-system-x86_64 -hda win10_for_challenge.qcow2 -m 4096 -smp 4,cores=4 -enable-kvm -cpu Broadwell,+smep,+smap,+pcid -vnc :0,password -monitor stdio -device e1000,netdev=user.0 -netdev user,id=user.0,hostfwd=tcp::50216-:50216
```


+ You can use `change vnc passwd` to change password of VNC. 


+ The VM just for your final test. You also can use your VM to test it. But you need makesure the build version is same as 10.0.19042.630

## Remote Service

### Contact

+ You should fill the [form](http://52.69.230.107/) with follow information. 
	+ Note : This form is not the part of the Lucifer challenge. Please don't attack this website.
 

```
Team token: (Team token in Team profile)
IP: (Which ip do you want to connect to the challenge)
Contact: (Your email)
IRC(optional): (Nickname at #hitconctf)
```

+ After we receive the information, we will send email with service ip.
	+ We will also notify you at irc(if you have provided it) after we have sent email to you.
+ We will not accept more than 3 requests per team during HITCON CTF.
	+ Please make sure your exploit is work in local in the environment we provide first.
	+ You can only use the service in 15 minutes at a time.
	+ If it's BSOD, we won't restart it.

### Run

We will run qemu with follow command:

```
/usr/bin/qemu-system-x86_64 -hda windows_base.qcow2 -m 4096 -smp 4,cores=4 -enable-kvm -cpu Broadwell,+smep,+smap,+pcid -nographic -monitor /dev/null -loadvm ctf_snapshot -device e1000,netdev=user.0 -netdev user,id=user.0,hostfwd=tcp::{port}-:{port}
```


 + The snapshot just login ctf account and run C:\ctf\start.bat.
 + It will run `C:\ctf\cmd.exe` as Low integrity
 + You can `nc ip port` to connect the service
 + You can use `curl` to download your binary in `%TEMP%\Low` or `c:\ctf\tmp`.


