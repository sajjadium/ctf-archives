/*
 * DBG header file
 * Author: peternguyen93
 */

#ifndef DBG_H
#define DBG_H

#include <stdio.h>
#include <assert.h>

#ifdef DEBUG
#define DBG(fmt, ...) fprintf(stderr, "[DEV] " fmt, ##__VA_ARGS__)
#else
#define DBG(fmt, ...)
#endif

#define assert_ok_f(ok, fmt, ...) assert((ok)); if((ok)) { printf(fmt, ##__VA_ARGS__); }
#define assert_fail_f(ok, fmt, ...) if(!(ok)) { printf(fmt, ##__VA_ARGS__); assert(!(ok)); }

#define ERROR(fmt, ...) fprintf(stderr, fmt, ##__VA_ARGS__);

#endif
