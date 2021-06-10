### 
The binary provided is already patched to the ld-2.32.so in the current directory.

```
"LD_PRELOAD=./libc-2.32.so ./house-of-yet_another_house" or use pwntools . `process('./house-of-yet_another_house',env={'LD_PRELOAD':'./libc-2.32.so'})`
```
USE THE PROVIDED LIBC.

malloc.diff file contains the patch made to glibc.
Read the flag from /home/challenge/flag.txt when test exploit on remote. alarm(1000) is enough.
