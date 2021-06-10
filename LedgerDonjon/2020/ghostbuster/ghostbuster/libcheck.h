#pragma once

#include <stdbool.h>
#include <sys/types.h>

#define SECRET_SIZE	32

bool check_secret(uint8_t *p, size_t size);
extern uint8_t (*_xor)(uint8_t, uint8_t);
extern uint8_t (*_or)(uint8_t, uint8_t);
