#ifndef __GUARDIAN_HEADER__
#define __GUARDIAN_HEADER__

#define _GNU_SOURCE
#include<link.h>
#include<sys/auxv.h>
#include<errno.h>
#include<pthread.h>
#include"util.h"
#include"pathlib.h"

#define LIBGUARDIAN "/lib/x86_64-linux-gnu/x86_64/libguardian.so"

#define getLock(lock) pthread_mutex_lock((lock))
#define dropLock(lock) pthread_mutex_unlock((lock))

#define addLib(arrp, entry) arrAppend((arrp), (void*)(entry), sizeof(LIBENTRY), 1, libEntryCopy)
#define searchLib(arr, entry) (LIBENTRY*)arrSearch((arr), (void*)(entry), sizeof(LIBENTRY), libEntryEq)

#define addString(arrp, entry) arrAppend((arrp), (void*)(entry), sizeof(char*), 1, charPointerCopy)

typedef struct {
  uintptr_t *cookie;
  char *libname;
} LIBENTRY;

char *WHITELISTLIB[] = {
  LIBGUARDIAN,
  "/lib/x86_64-linux-gnu/libc.so.6",
  "/lib/x86_64-linux-gnu/libtinfo.so.6",
  "/lib/x86_64-linux-gnu/libselinux.so.1",
  "/lib/x86_64-linux-gnu/libpcre2-8.so.0",
  NULL
};

char *WHITELISTEXE[] = {
  "/usr/bin/bash",
  "/usr/bin/ls",
  "/usr/bin/cat",
  NULL
};

ARR *LOADEDLIB = NULL;
pthread_mutex_t LOADEDLIBLOCK = PTHREAD_MUTEX_INITIALIZER;

void libEntryCopy(void *dst, void *src, size_t cnt);
bool libEntryEq(void *e1, void *e2);

void charPointerCopy(void *dst, void *src, size_t cnt);
int intFail();


#endif
