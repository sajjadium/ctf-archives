A classic crackme.

libcrypt and libscrypt are required. On Debian-based system :

    # apt update
    # apt install libcrypt1 libscrypt-kdf1

If a packaged version of libscrypt is not available for your system, the library used to build the binary is given. Usage :

    $ LD_PRELOAD=./libscrypt-kdf.so.1.0.0 ./pincrack ...

