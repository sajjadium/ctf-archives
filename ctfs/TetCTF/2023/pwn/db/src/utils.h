/*
 * Utilities Function Exports
 * Implement some functions support to read/write, parse number from stdin
 */

#ifndef UTILS_H
#define UTILS_H

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

__BEGIN_DECLS

void read_str(char *buffer, size_t max_size);
void read_buf(char *buffer, size_t size);

uint32_t read_uint32();
uint64_t read_uint64();

__END_DECLS

#endif
