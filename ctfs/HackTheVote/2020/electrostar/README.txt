Here we have an IPC signed module based ballot counting machine.
This allows modules to be sandboxed for extra security (see sandbox.h)

The server will be running the binary such as in `server.sh`

You can start the system with this:
```
./machine modules/init_module.img.sig
```

Flag 1 and 2 can be gotten with special IPC calls.
Flag 3 will be execute only and you need a shell.

