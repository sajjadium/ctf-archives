# myfuse

我把 xv6 的文件系统复制到了 libfuse 上，现在你可以在一个真实的 Linux 操作系统上使用它了！

我甚至写了一些“单元”测试来说服我自己我实现的没有问题，但是在实际运行时它经常崩溃。我觉得这个程序当前是可以利用的，你可以帮我执行他的后门吗？

## some tips

- **非常重要：** 服务器的 **ASLR 的级别为 1**，也就是说目标服务器上执行了 `echo 1 > /proc/sys/kernel/randomize_va_space`

- 这些链接可能非常有用:
  - https://pdos.csail.mit.edu/6.S081/2021/xv6/book-riscv-rev2.pdf
  - https://github.com/libfuse/libfuse/blob/master/example/hello.c
  - https://www.cs.hmc.edu/~geoff/classes/hmc.cs135.201109/homework/fuse/fuse_doc.html

- 你可能会发现它的漏洞主要在堆上，所以在你一头埋入投入源码前，使用 asan 这样的工具先找到 bug 可能非常有效

- 虽然他的漏洞主要在堆上，但是**不需要用到任何 house of XX 的技巧**。

- fuse 是通过一个叫 `fuse_server` 的 shell 脚本启动的，如果你把 fuse server 弄崩溃了，他会自动重启。（这意味着你可以**分多个阶段来对本题进行利用**，同时你可能会发现利用外存的存储持久性可以有效帮助你的利用）

- 各种偏移可能很易变，所以我提供了完整的 docker file（配置文件可能看起来比较复杂，主要是因为做不到给每支队伍单独分配一个 docker）。建议先在本地完成对一个有完整调试信息的目标完成利用，再针对远程环境修改偏移。