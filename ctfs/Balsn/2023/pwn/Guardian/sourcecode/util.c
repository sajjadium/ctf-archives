#include"util.h"

void printError(char *msg) {
  puts(msg);
  _exit(0);
}

void *safeCalloc(size_t size) {
  void *buf = calloc(size, 1);
  if (buf == NULL) {
    printError("safeCalloc failed");
  }
  return buf;
}

void *safeRealloc(void *orig, size_t size) {
  void *buf = realloc(orig, size);
  if (buf == NULL) {
    printError("safeRealloc failed");
  }
  return buf;
}

void arrAppend(ARR **arrp, void *newEntries, size_t entrySize, size_t newEntriesCnt, void (*cpFunc)(void*, void*, size_t)) {
  if (*arrp == NULL) {
    *arrp = safeCalloc(sizeof(ARR));
  }
  ARR *arr = *arrp;
  size_t newCnt = arr->cnt + newEntriesCnt;
  if (newCnt <= arr->cnt) {
    printError("arrConcat failed");
  }
  if (arr->capacity < newCnt) {
    size_t newCapacity = arr->capacity == 0 ? 16 : arr->capacity * 2;
    while (newCapacity < newCnt) {
      newCapacity = newCapacity * 2;
      if (newCapacity <= arr->capacity) {
        printError("arrInsert failed");
      }
    }
    size_t newSize = newCapacity * entrySize;
    if ((newSize / newCapacity) != entrySize) {
      printError("arrInsert failed");
    }
    arr->entries = safeRealloc(arr->entries, newSize);
    arr->capacity = newCapacity;
  }
  cpFunc(&(((char*)arr->entries)[arr->cnt * entrySize]), newEntries, newEntriesCnt);
  arr->cnt += newEntriesCnt;
  return; 
}

void *arrGet(ARR *arr, size_t idx, size_t entrySize) {
  if ((arr == NULL) || (arr->cnt <= idx)) {
    printError("arrGet failed");
  }
  return &(((char*)arr->entries)[idx * entrySize]);
}

void *arrSearch(ARR *arr, void *targetEntry, size_t entrySize, bool (*eqFunc)(void*, void*)) {
  for (size_t idx = 0; idx < arr->cnt; idx++) {
    void *curEntry = arrGet(arr, idx, entrySize);
    if (eqFunc(curEntry, targetEntry)) {
      return curEntry;
    }
  }
  return NULL;
}
