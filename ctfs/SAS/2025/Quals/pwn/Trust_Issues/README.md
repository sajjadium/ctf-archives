Target system is a secure-world Trustlet running inside a TEE. The

 codebase is signed, verified, and marked "production

 ready."

 But something doesn't add up.

 Your mission today, if you choose to accept it, is to do what the

 auditors couldn't, wouldn't or were too lazy to do, press

 F5 and find the flag.

 The flag is stored as a secure object. The id for that object is

 flag.

 Note: for easier debugging, here's how you can connect GDB to

 the QEMU instance. If you start QEMU with the -s option, a GDB

 server will be available at 127.0.0.1:1234. Since ASLR is disabled,

 you can attach using:

 gdb-multiarch -ex 'target remote 127.0.0.1:1234' -ex

 'add-symbol-file 41414141-7472-7573-745f-697373756573.elf

 0x117000'

 This allows you to debug the Trustlet like a regular user-space

 application - set breakpoints, inspect memory, and step through

 execution.
