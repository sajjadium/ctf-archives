#include <sys/syscall.h>
#include "seccomp.h"

#define NR 0
#define ARCH 4

; build with bpfc -p -i ./bin/filter.s

ld [ARCH]
jne #AUDIT_ARCH_X86_64, kill
ld [NR]

jeq #__NR_read, allow
jeq #__NR_write, allow
jeq #__NR_open, allow

jeq #__NR_exit, allow
jeq #__NR_exit_group, allow
jeq #__NR_mmap, mmap

jmp kill

; ensure nx on mmap
mmap:
; read prot arg
ld [32]
jset #0x4, kill

allow: ret #SECCOMP_RET_ALLOW
kill: ret #SECCOMP_RET_KILL