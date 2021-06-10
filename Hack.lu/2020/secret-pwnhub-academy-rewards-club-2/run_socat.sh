#!/bin/bash
binary=sparc-2
socat_args=",pty,rawer,stderr,echo=0,su=ctf"
if [ $# -lt 1 ]; then
    # Default, standalone case
    socat tcp-listen:4444,reuseaddr,fork exec:"qemu-sparc-static $binary"$socat_args
else
    # Pass an argument to expose GDB server on port 1234
    socat tcp-listen:4444,reuseaddr,fork exec:"qemu-sparc-static -g 1234 $binary"$socat_args > /dev/null &
    gdb-multiarch -ex "target remote localhost:1234" -ex "b main" -ex "continue" $binary
fi
