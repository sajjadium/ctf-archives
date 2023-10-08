#ifndef __LIB_HEADER__
#define __LIB_HEADER__

#include <stddef.h>
#include <stdint.h>
#include "syscall.h"

#define PAGE_SHIFT 12
#define PAGE_SIZE 0x1000

void abort(uint8_t *msg);
uint64_t atonum(uint8_t *buf);
void numtoa(uint64_t num, uint8_t *buf);
void hexencode(uint8_t *inbuf, uint64_t insize, uint8_t *outbuf, uint64_t outsize);
void hexdecode(uint8_t *inbuf, uint64_t insize, uint8_t *outbuf, uint64_t outsize);
uint64_t strlen(uint8_t *msg);
void *memcpy(uint8_t *dst, uint8_t *src, uint64_t size);
uint64_t readSizeHex(uint8_t *buf, uint64_t size);
uint64_t readSize(uint8_t *buf, uint64_t size);
uint64_t readNum();
uint64_t readLine(uint8_t *buf, uint64_t bufsize);
void printNum(uint64_t num);
void printStr(uint8_t *buf);
void printSize(uint8_t *buf, uint64_t size);
void puts(uint8_t *buf);
void setChunkSize(void *chunk, uint64_t size);
uint64_t getChunkSize(void *chunk);
void *malloc(uint64_t size);
void free(void *buf);

#endif
