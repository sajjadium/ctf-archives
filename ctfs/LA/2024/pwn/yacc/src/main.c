#define EXTERN
#include "calc.h"

char *outpath = "/tmp/a.out";
unsigned char filter[] = {32, 0, 0, 0, 4, 0, 0, 0, 21, 0, 0, 12, 62, 0, 0, 192, 32, 0, 0, 0, 0, 0, 0, 0, 21, 0, 9, 0, 2, 0, 0, 0, 21, 0, 8, 0, 0, 0, 0, 0, 21, 0, 7, 0, 1, 0, 0, 0, 21, 0, 6, 0, 60, 0, 0, 0, 21, 0, 5, 0, 15, 0, 0, 0, 21, 0, 0, 5, 59, 0, 0, 0, 32, 0, 0, 0, 20, 0, 0, 0, 21, 0, 0, 3, 105, 105, 105, 105, 32, 0, 0, 0, 16, 0, 0, 0, 21, 0, 0, 1, 105, 105, 105, 105, 6, 0, 0, 0, 0, 0, 255, 127, 6, 0, 0, 0, 0, 0, 0, 0};
struct prog {
	unsigned short len;
	unsigned char *filter;
} rule = {
	.len = sizeof(filter) >> 3,
	.filter = filter,
};

int main()
{
	outfile = fopen(outpath, "w");
	if(!outfile) {
		perror("fopen");
		return 1;
	}
	if(chmod(outpath, 0700)) {
		perror("chmod");
		return 1;
	}
	if(read(0, inpbuf, INPSZ) < 0) {
		perror("read");
		return 1;
	}
	compile();
	fclose(outfile);
	*(int*)(filter+84) = (unsigned long)outpath >> 32;
	*(int*)(filter+100) = (unsigned long)outpath;
	if(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) {
		perror("prctl(PR_SET_NO_NEW_PRIVS)");
		return 1;
	}
	if(prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0) {
		perror("prctl(PR_SET_SECCOMP)");
		return 1;
	}
	char *args[] = {outpath, 0};
	execve(outpath, args, NULL);
}
