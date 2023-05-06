#include <stdio.h>
#include <sys/mman.h>
#include <seccomp.h>


int get_file_size(FILE *fp) {
	fseek(fp, 0L, SEEK_END);
	int sz = ftell(fp);
	fseek(fp, 0L, SEEK_SET);
	return sz;
}

void init_syscall_filter() {
	// allow only four syscalls: open, read, write and exit
	// the process is killed on execution of any other syscall
	scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
	seccomp_load(ctx);
}

int main(int argc, char **argv) {
	if (argc != 2) {
		puts("./shellcode_executor <file>");
		return 1;
	}

	char *shellcode_file = argv[1];

	FILE *fp = fopen(shellcode_file, "r");
	if (fp == NULL) {
		puts("File not found");
		return 1;
	}
	
	unsigned int file_size = get_file_size(fp);

	void *shellcode_ptr = mmap(NULL, 0x1000, PROT_READ|PROT_WRITE, MAP_ANON|MAP_PRIVATE, -1, 0);
	fread(shellcode_ptr, file_size + 1, 1, fp);

	mprotect(shellcode_ptr, 0x1000, PROT_READ | PROT_EXEC);
	
	init_syscall_filter();
	void (*shellcode)() = (void(*)())shellcode_ptr;
	shellcode();
	return 0;
}
