#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/sched.h>
#include <linux/syscalls.h>
#include <linux/string.h>

char corctf_note[0x10] = {0};

SYSCALL_DEFINE2(corctf_write_note, char *, addr, size_t, size)
{
     if (size > sizeof(corctf_note) - 1)
          return -EINVAL;
     return copy_from_user(corctf_note, addr, size);
}

SYSCALL_DEFINE4(corctf_read_note, char *, addr, uint64_t, idx1, uint64_t, idx2, uint64_t, stride)
{
     uint64_t off = corctf_note[idx1];
     if (strlen(corctf_note) > idx1 && strlen(corctf_note) > idx2) {
          return copy_to_user(addr + (off << stride), corctf_note + idx2, 1);
     } 
     else {
          return -EINVAL;
     }
}