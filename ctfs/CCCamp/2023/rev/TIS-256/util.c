#include "util.h"

#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>

void
die(const char *fmt, ...)
{
	va_list ap;

	if (cleanup) cleanup();

	va_start(ap, fmt);
	fprintf(stderr, "%s: ", progname);
	vfprintf(stderr, fmt, ap);
	if (*fmt && fmt[strlen(fmt)-1] == ':') {
		fputc(' ', stderr);
		perror(NULL);
	} else {
		fputc('\n', stderr);
	}
	va_end(ap);

	exit(1);
}

size_t
strdcpy(char *dst, const char *src, size_t n)
{
	strncpy(dst, src, n);
	return strlen(src);
}

size_t
strdcat(char *dst, const char *src, size_t n)
{
	size_t len;

	len = strlen(dst);
	strncpy(dst + len, src, n - len);
	return strlen(src);
}
