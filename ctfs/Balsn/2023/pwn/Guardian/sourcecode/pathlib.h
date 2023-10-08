#ifndef __PATHLIB_HEADER__
#define __PATHLIB_HEADER__

#include<string.h>
#include<limits.h>
#include"util.h"

#define pushPath(arrp, entries, length) arrAppend((arrp), (void*)(entries), sizeof(char), length, (void(*)(void *, void *, size_t))memcpy)
#define popPath(arr, entries) do { \
                                if ((arr)->cnt < (entries)) { \
                                  printError("popPath failed"); \
                                } \
                                (arr)->cnt-=(entries); \
                              } while(0)
#define getPath(arr, idx) *(char*)arrGet((arr), idx, sizeof(char)) 

#define nullTerminatePath(arr) do { \
                                 pushPath(&(arr), "\x00", 1); \
                                 popPath((arr), 1); \
                               } while(0)

typedef enum {
  StartDir,
  Body,
  Done,
} PATHSTATE;

typedef enum {
  None,
  Normal,
  CurDir,
  ParentDir,
  RootDir,
} COMPONENTTYPE;

typedef struct {
  char *start;
  size_t length;
  COMPONENTTYPE type;
} PATHCOMPONENT;

typedef struct {
  bool hasRoot;
  bool includeCurDir;
  char *start;
  char *end;
  char *cursor;
  PATHSTATE state;
} PATHITERATOR;

char *resolvePath(char *origPath, bool isDir);

#endif
