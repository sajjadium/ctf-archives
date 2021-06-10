#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <sys/ptrace.h>
#include <sys/prctl.h>
#include <stddef.h>
#include <sys/syscall.h>

#define ArchField offsetof(struct seccomp_data, arch)
#define Syscall offsetof(struct seccomp_data, nr)

#define Reject(syscall) \
	BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_IMM, __NR_##syscall, 0, 1), \
	BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_KILL) \


struct sock_filter sock_filter[] = {
	BPF_STMT(BPF_LD + BPF_W + BPF_ABS, ArchField),
	BPF_JUMP(BPF_JMP + BPF_JEQ + BPF_IMM, AUDIT_ARCH_X86_64, 1, 0),
	BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_KILL),
	BPF_STMT(BPF_LD + BPF_W + BPF_ABS, Syscall),
	
	Reject(execve),
	Reject(execveat),
	Reject(open),
	Reject(dup),
	Reject(dup2),
	Reject(dup3),
	Reject(prctl),
	Reject(creat),
	Reject(fork),
	Reject(process_vm_readv),
	Reject(process_vm_writev),

	BPF_STMT(BPF_RET + BPF_K, SECCOMP_RET_ALLOW)
};

struct sock_fprog sock_fprog = {
	.len = sizeof(sock_filter)/sizeof(sock_filter[0]),
	.filter = sock_filter
};


void seccomp_apply(void) {
	if(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
		puts("prctl no new privs failed!");
		exit(-1);
	}

	if(prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &sock_fprog) == -1) {
		puts("Seccomp load failed!");
		exit(-1);
	}
}

void __attribute__((constructor)) init() {
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	seccomp_apply();
	alarm(60*4);
}

int main() {
	char buf[0x108];
	unsigned long p = buf;
	puts("It may be helpful: ");
	printf("0x%x\n", (p & 0xffff));
	memset(buf, 0, 0x108);
	close(1);
	read(0, buf, 0x100);
	printf(buf);
	return 0;
}
