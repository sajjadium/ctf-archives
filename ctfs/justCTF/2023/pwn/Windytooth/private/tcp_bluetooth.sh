#!/bin/sh
timeout -k60 59 strace -f --signal=none --quiet=all --seccomp-bpf -esocket,bind --inject=socket,bind:retval=0 /zephyr.elf --bt-dev=hci0
