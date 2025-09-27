#include "compat.h"
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include "heap.h"


void* cg_malloc(size_t size) {
	return cage_malloc(NULL, size);
}

void cg_free(void* obj) {
	return cage_free(NULL, obj);
}

void* cg_realloc(void* obj, size_t new_size) {
	return cage_realloc(NULL, obj, new_size);
}

void* cg_calloc(size_t count, size_t size) {
	if(size >= SIZE_MAX / count) {
		return NULL;
	}
	
	void* obj = cg_malloc(count * size);
	if(obj) {
		memset(obj, 0, count * size);
	}
	return obj;
}

char* cg_strdup(const char* str) {
	if(str == NULL) {
		return NULL;
	}
	
	size_t len = strlen(str);
	char* copy = cg_malloc(len + 1);
	memcpy(copy, str, len + 1);
	return copy;
}

char* cg_strndup(const char* str, size_t maxchars) {
	if(str == NULL) {
		return NULL;
	}
	
	size_t len = strnlen(str, maxchars);
	char* copy = cg_malloc(len + 1);
	memcpy(copy, str, len);
	copy[len] = '\0';
	return copy;
}

int cg_vasprintf(char** ret, const char* format, va_list ap) {
	*ret = NULL;
	
	va_list ap_copy;
	va_copy(ap_copy, ap);
	int retlen = vsnprintf(NULL, 0, format, ap_copy);
	va_end(ap_copy);
	
	if(retlen < 0) {
		return retlen;
	}
	
	char* buf = cg_malloc((size_t)retlen + 1);
	if(!buf) {
		return -1;
	}
	
	*ret = buf;
	return vsnprintf(buf, (size_t)retlen + 1, format, ap);
}

int cg_asprintf(char** ret, const char* format, ...) {
	va_list ap;
	va_start(ap, format);
	
	int rv = cg_vasprintf(ret, format, ap);
	
	va_end(ap);
	
	return rv;
}
