#include <elk.h>
#include <fcntl.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_SZ 0x1000

static ssize_t read_until_delim(int fd, char *buf, size_t count, int delim) {
	ssize_t n = 0;
	size_t off = 0;
	do {
		n = read(fd, buf+off, 1);
		if (delim != 0 && buf[off] == delim) {
			buf[off] = 0;
			break;
		}
		if (n > 0) { off += n; }
	} while (n > 0 && off < count);
	return off;
}

static bool read_uint(unsigned int *v) {
	if (!v) { return false; }
	char buf[11];
	memset(buf, 0, sizeof(buf));
	if (read_until_delim(0, buf, sizeof(buf)-1, '\n') < 0) {
		return false;
	}
	return sscanf(buf, "%u", v) == 1;
}

int main(int argc, char **argv) {
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
	const unsigned int mem_sz = 2*MAX_SZ;
	void *mem = alloca(mem_sz);
	if (mem == 0) { return EXIT_FAILURE; }

	volatile int show_flag = 0xdeadbeef;
	struct js *js = js_create(mem, mem_sz);
	if (js == 0) {
		return EXIT_FAILURE;
	}

	printf("how many bytes will you be sending? (%u max) ", MAX_SZ);
	unsigned int length = 0;
	if (!read_uint(&length)) {
		return EXIT_FAILURE;
	}
	if (length > MAX_SZ) {
		return EXIT_FAILURE;
	}
	char *script = calloc(1, length);
	if (script == 0) { return EXIT_FAILURE; }
	printf("feed me %u bytes\n", length);
	if (read_until_delim(0, script, length-1, 0) < 0) {
		return EXIT_FAILURE;
	}

	jsval_t v = js_eval(js, script, ~0U);
	printf("result: %s\n", js_str(js, v));

	if (show_flag == 0x41414141) {
		int fd = open("flag", O_RDONLY);
		if (fd == -1) {
			printf("uh oh, flag not found. contact organizers!\n");
			return EXIT_FAILURE;
		}
		char flag[50];
		flag[read_until_delim(fd, flag, sizeof(flag), '\n')] = 0;
		printf("flag: %s\n", flag);
	}

	return EXIT_SUCCESS;
}
