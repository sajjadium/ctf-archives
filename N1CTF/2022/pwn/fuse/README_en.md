# myfuse

I copied xv6's filesystem part to libfuse, now you can use it on a real linux machine!

I even wrote some "unit" test to confirm myself I copied it right, but it keeps crashing. I think it is exploitable, can you help me to run its backdoor?

## some tips

- **very important**: the **ASLR level is 1**, i.e., the target server has executed `echo 1 > /proc/sys/kernel/randomize_va_space`

- this links might be useful:
  - https://pdos.csail.mit.edu/6.S081/2021/xv6/book-riscv-rev2.pdf
  - https://github.com/libfuse/libfuse/blob/master/example/hello.c
  - https://www.cs.hmc.edu/~geoff/classes/hmc.cs135.201109/homework/fuse/fuse_doc.html

- you might find it is a heap based challenge, so asan is useful to find the bug before you dive into the source code.

- though this is a heap challenge, **no house of XX technic is needed**.

- the fuse is started by the shell script `fuse_server`. it will automatically restart the fuse if you crashed it. (this means **you can solve this challenge by multiple stages**, and you might find it useful to exploit the persistent of disk storage)

- the offsets can be really volatile. so the full docker file is provided (you might find the configuration can be quite complicated, this is mainly because we can't provide a single separate docker for each team). It is recommend to first exploit a local debug version (with full debug information) and then change some offset to break the server's version