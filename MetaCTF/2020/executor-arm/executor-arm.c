#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <seccomp.h>
#include <sys/prctl.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>

#define LENGTH 128

void sandbox(){
	scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
	if (ctx == NULL) {
		printf("seccomp error\n");
		exit(0);
	}

	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(getdents64), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
	seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);

	if (seccomp_load(ctx) < 0){
		seccomp_release(ctx);
		exit(0);
	}
	seccomp_release(ctx);
}

void handler(int sig) {
	exit(-2);
}

char code[1000];

int main(int argc, char* argv[]){

	setbuf(stdout, 0);
	setbuf(stdin, 0);

	puts("Welcome to the executor! Now powered by Aarch64!");
	puts("Wanna learn/practice how to write ARM64 assembly? This challenge is for you!");
	puts("We have added limits on what syscalls you can use. Good luck!");
	puts("Note: The flag is inside a file that's in the current directory. However, you'll need to find the flag filename first.");
	puts("Enter your code below:");

	signal(SIGALRM, handler);

	alarm(30);

	memset(&code, 0, 1000); 
	read(0, &code, 1000);
	puts("Processing code...");

	sandbox();

	(*(void(*)()) code)();

	return 0;
}
