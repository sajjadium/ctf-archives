#ifndef CAGE_COMPAT_H
#define CAGE_COMPAT_H

#include <stddef.h>
#include <stdarg.h>

void* cg_malloc(size_t size) __attribute__((__warn_unused_result__)) __attribute__((__alloc_size__(1)));
void cg_free(void* obj);
void* cg_realloc(void* obj, size_t new_size) __attribute__((__warn_unused_result__)) __attribute__((__alloc_size__(2)));
void* cg_calloc(size_t count, size_t size) __attribute__((__warn_unused_result__)) __attribute__((__alloc_size__(1, 2)));
char* cg_strdup(const char* str) __attribute__((__warn_unused_result__));
char* cg_strndup(const char* str, size_t maxchars) __attribute__((__warn_unused_result__));
int cg_vasprintf(char** ret, const char* format, va_list ap) __attribute__((__format__(printf, 2, 0)));
int cg_asprintf(char** ret, const char* format, ...) __attribute__((__format__(printf, 2, 3)));

#endif /* CAGE_COMPAT_H */
