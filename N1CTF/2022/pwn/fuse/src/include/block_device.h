#pragma once
#include "param.h"

// return: n bytes write
int write_block_raw(uint block_id, const u_char* buf);

// return: n bytes read
int read_block_raw(uint block_id, u_char* buf);
int read_block_raw_nbytes(uint block_id, u_char* buf, uint nbytes);

void block_device_init(const char* path_to_device);