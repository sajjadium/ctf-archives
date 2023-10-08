#include "lib.h"

void abort(uint8_t *msg) {
  puts(msg);
  exit(0);
}

uint64_t atonum(uint8_t *buf) {
  uint64_t res = 0;
  for(; '0' <= *buf && '9' >= *buf; buf++) {
    res = res * 10 + (*buf - '0');
  }
  return res;
}

void numtoa(uint64_t num, uint8_t *buf) {
  uint64_t idx;
  if (num == 0) {
    buf[0] = '0';
    buf[1] = '\0';
    return;
  }
  for (idx = 0; num > 0; num /= 10, idx++) {
    buf[idx] = '0' + num % 10;
  }
  buf[idx--] = '\0';
  for (uint64_t i = 0; i < idx; i++, idx--) {
    uint8_t tmp = buf[i];
    buf[i] = buf[idx];
    buf[idx] = tmp;
  }
  return;
}

void hexencode(uint8_t *inbuf, uint64_t insize, uint8_t *outbuf, uint64_t outsize) {
  if (outsize < (insize * 2)) {
    abort("hexencode output buffer too small");
  }
  for (uint64_t i = 0; i < insize; i++) {
    uint8_t up = inbuf[i] >> 4;
    uint8_t lo = inbuf[i] & 0xf;
    if (up >= 10) {
      outbuf[i * 2] = 'a' + up - 10;
    } else {
      outbuf[i * 2] = '0' + up;
    }
    if (lo >= 10) {
      outbuf[i * 2 + 1] = 'a' + lo - 10;
    } else {
      outbuf[i * 2 + 1] = '0' + lo;
    }
  }
  return;
}

void hexdecode(uint8_t *inbuf, uint64_t insize, uint8_t *outbuf, uint64_t outsize) {
  if (((insize % 2) != 0 ) || (outsize < (insize / 2))) {
    abort("hexdecode output buffer too small");
  }
  for (uint64_t i = 0; i < insize; i += 2) {
    uint8_t up = inbuf[i];
    uint8_t lo = inbuf[i + 1];
    uint8_t val = 0;
    if (up >= 'a') {
      val = (up - 'a' + 10) << 4;
    } else {
      val = (up - '0') << 4;
    }
    if (lo >= 'a') {
      val |= (lo - 'a' + 10);
    } else {
      val |= (lo - '0');
    }
    outbuf[i / 2] = val;
  }
  return;
}

uint64_t strlen(uint8_t *msg) {
  uint8_t *c = msg;
  uint64_t l = 0; 
  for (c = msg; *c != '\0'; c++, l++);
  return l;
}

void *memcpy(uint8_t *dst, uint8_t *src, uint64_t size) {
  uint8_t *origBuf = dst;
  for (; size > 0; size--, dst++, src++) {
    *dst = *src;
  }
  return origBuf;
}

uint64_t readSizeHex(uint8_t *buf, uint64_t size) {
  uint8_t tmpbuf[size * 2];
  readSize(tmpbuf, size * 2);
  hexdecode(tmpbuf, size * 2, buf, size);
  return size;
}

uint64_t readSize(uint8_t *buf, uint64_t size) {
  //uint8_t *origBuf = buf;
  for(; size > 0; buf++, size--) {
    if (((int)read(STDIN_FILENO, buf, 1)) <= 0) {
      abort("readSize failed");
    }
  }
  return size; 
}

uint64_t readNum() {
  uint8_t buf[0x100];
  readLine(buf, sizeof(buf) - 1);
  return atonum(buf);
}

uint64_t readLine(uint8_t *buf, uint64_t bufsize) {
  uint8_t *origBuf = buf;
  for(; bufsize > 0; buf++, bufsize--) {
    if (((int)read(STDIN_FILENO, buf, 1)) <= 0) {
      abort("readLine failed");
    }
    if (*buf == '\n') {
      return buf - origBuf;
    }
  }
  return buf - origBuf;
}

void printNum(uint64_t num) {
  uint8_t buf[0x20];
  numtoa(num, buf);
  printStr(buf);
  return;
}

void printStr(uint8_t *buf) {
  write(STDOUT_FILENO, buf, strlen(buf));
  return;
}

void printSize(uint8_t *buf, uint64_t size) {
  write(STDOUT_FILENO, buf, size);
  return;
}

void puts(uint8_t *buf) {
  printStr(buf);
  write(STDOUT_FILENO, "\n", 1);
  return;
}

void setChunkSize(void *chunk, uint64_t size) {
  ((uint64_t*)chunk)[-2] = size;
  return;
}

uint64_t getChunkSize(void *chunk) {
  return ((uint64_t*)chunk)[-2];
}

void *malloc(uint64_t size) {
  size += sizeof(uint64_t) * 2;
  uint64_t nsize = ((size + (PAGE_SIZE - 1)) >> PAGE_SHIFT) << PAGE_SHIFT;
  if (nsize < size) {
    return NULL;
  }
  void *res = mmap(NULL, nsize, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  if (res == (void*)-1) {
    return NULL;
  }
  res = &(((uint64_t*)res)[2]);
  setChunkSize(res, nsize);
  return res;
}

void free(void *buf) {
  uint64_t size = getChunkSize(buf);
  munmap(&(((uint64_t*)buf)[-2]), size);
  return;
}
