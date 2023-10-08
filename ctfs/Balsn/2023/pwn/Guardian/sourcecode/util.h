#ifndef __UTIL_HEADER__
#define __UTIL_HEADER__

#include<stdio.h>
#include<stdint.h>
#include<stdbool.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<assert.h>

#ifdef DEBUG
  #define DEBUGPRINTF(fmt, ...) printf((fmt), ##__VA_ARGS__)
#else
  #define DEBUGPRINTF(fmt, ...)
#endif

typedef struct {
  size_t capacity;
  size_t cnt;
  void *entries;
} ARR;

void printError(char *msg);

void *safeCalloc(size_t size);
void *safeRealloc(void *orig, size_t size);

void arrAppend(ARR **arrp, void *newEntries, size_t entrySize, size_t newEntriesCnt, void (*cpFunc)(void*, void*, size_t));
void *arrGet(ARR *arr, size_t idx, size_t entrySize);
void *arrSearch(ARR *arr, void *targetEntry, size_t entrySize, bool (*eqFunc)(void*, void*));

#endif
