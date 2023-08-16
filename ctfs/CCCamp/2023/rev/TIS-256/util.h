#pragma once

#include <stddef.h>

#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MAX(a, b) ((a) < (b) ? (b) : (a))
#define ABS(a) ((a) > 0 ? (a) : -(a))

__attribute__((noreturn))
__attribute__((format(printf, 1, 2)))
void die(const char *fmt, ...);

size_t strdcpy(char *dst, const char *src, size_t n);
size_t strdcat(char *dst, const char *src, size_t n);

extern const char *progname;
extern int (*cleanup)(void);
