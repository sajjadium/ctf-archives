/*
 * Implementation of utils.h
 * Author: peternguyen93
 */
#include "utils.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

void read_str(char *buffer, size_t max_size)
{
	size_t i = 0;

	assert(buffer != NULL && max_size >= 1);

	if(max_size == 1){
		// handle case when max_size is one
		buffer[0] = '\0';
		return;
	}

	while(i < max_size - 1){
		char ch = fgetc(stdin);
		if(ch == '\n') {
			// if user input enter, stop the loop return buffer to user
			buffer[i] = '\0'; // NULL the buffer
			break;
		}
		buffer[i++] = ch; //write char to buffer
	}

	buffer[i] = '\0'; // make sure we added NULL in the end of string
}

void read_buf(char *buffer, size_t size)
{
	assert(buffer != NULL && size > 0);
	fread(buffer, size, 1, stdin);
}

uint32_t read_uint32()
{
	char buf[32];
	read_str(buf, sizeof(buf));
	return strtoul(buf, NULL, 10);
}

uint64_t read_uint64()
{
	char buf[64];
	read_str(buf, sizeof(buf));
	return strtoull(buf, NULL, 10);
}
