Antarctica syndrome

I tried to add a simple qqemu.Pid packet to QEMU's gdbstub to expose the process's PID via getpid(). The patch got rejected — apparently, it was an "information leak"

But… are they really sure the gdbstub doesn’t already allow far worse things?

Author: patryk4815
