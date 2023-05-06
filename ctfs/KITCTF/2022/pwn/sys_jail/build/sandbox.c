#include <stdio.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <string.h>


#define SYS_JAIL 451

typedef struct jail_info {
	int requested_uid;
	unsigned int requestor_uid;
	unsigned long long token;
} jail_info;

int main() {
	puts("Going to jail...");
	jail_info info = {.requested_uid = -1};
	unsigned long long ret = syscall(SYS_JAIL, &info);
	printf("UID: %d\n", getuid());
	
	pid_t pid = fork();

	if (pid < 0) {
       printf("Fork failed\n");
       return 1;
	} else if (pid == 0) {
		system("/bin/sh");
	} else {
		wait(NULL);
	}
	return 0;
}
