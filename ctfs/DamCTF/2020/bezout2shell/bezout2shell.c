#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <inttypes.h>

#include <linux/seccomp.h>
#include <sys/prctl.h>

typedef __int128_t int128_t;

#define CHECKS 256

typedef struct
{
	uint64_t addr;
	int64_t inverses[CHECKS];
} shared_data;

uint64_t moduli[CHECKS];

int64_t get_random()
{
	int64_t out;

	FILE* urandom = fopen("/dev/urandom", "rb");
	if (!urandom)
		exit(EXIT_FAILURE);
	if (fread(&out, sizeof(int64_t), 1, urandom) != 1)
		exit(EXIT_FAILURE);
	if (fclose(urandom))
		exit(EXIT_FAILURE);

	return out;
}

void sys_exit(int status, void* arg)
{
	syscall(SYS_exit, status);
}

void parent_proc(shared_data* shared, pid_t child)
{
	int exit_status;
	if (waitpid(child, &exit_status, 0) != child)
		exit(EXIT_FAILURE);

	for (int i = 0; i < CHECKS; i++)
	{
		uint64_t addr = shared->addr;
		int64_t inverse = shared->inverses[i];
		uint64_t modulus = moduli[i];

		if (abs(inverse) >= modulus)
			exit(EXIT_FAILURE);

		int64_t gcd = ((int128_t) addr * inverse) % modulus;
		if (gcd < 0)
			gcd += moduli[i];

		// Check that the result is really the gcd.
		if (addr % gcd != 0 || modulus % gcd != 0)
			exit(EXIT_FAILURE);
	}

	// Jump!
	if (shared->addr > 1)
		((void (*)(int, int, int)) shared->addr)(0, 0, 0);
}

void child_proc(shared_data* shared, size_t limit)
{
	unsigned char buffer[0x10];
	printf("Stack leak: %p\n", buffer);

	printf("Shellcode please.\n");
	read(STDIN_FILENO, buffer, limit);

	if (close(STDIN_FILENO) || close(STDOUT_FILENO) || close(STDERR_FILENO))
		exit(EXIT_FAILURE);

	prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT);

	shared->addr = 1;
	for (int i = 0; i < CHECKS; i++)
		shared->inverses[i] = 1;
}

int main()
{
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);

	// libc calls exit_group instead of exit by default, but that system call is
	// disabled by seccomp. Use exit instead.
	on_exit(sys_exit, NULL);

	const char* hours_str = getenv("HOURS_SINCE_START");
	if (hours_str == NULL)
		exit(EXIT_FAILURE);
	int hours = atoi(hours_str);
	if (hours < 0)
		exit(EXIT_FAILURE);
	size_t limit = 0x20 + 3 * (size_t) hours;
	printf("Current size limit: %ld\n\n", limit);

	for (int i = 0; i < CHECKS; i++)
		moduli[i] = get_random() & 0x7fffffffffffffff;

	shared_data* shared = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);

	pid_t child = fork();
	if (child)
		parent_proc(shared, child);
	else
		child_proc(shared, limit);

	return EXIT_SUCCESS;
}
