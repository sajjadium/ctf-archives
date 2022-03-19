#ifndef __REDIS_HEADER__
#define __REDIS_HEADER__

#include "resp.h"

typedef struct {
  const char *name;
  resp_t* (*run)(const resp_array_t*);
  resp_t* (*help)(void);
} redis_command_t;

typedef struct redis_db_t {
  struct redis_db_t* next;
  struct redis_db_t* prev;
  resp_t* key;
  resp_t* value;
} redis_db_t;

extern redis_command_t redis_cmd_list[];
extern int redis_cmd_count;

void redis_clear(void);
redis_db_t* redis_get(const resp_t*);
int redis_insert(const resp_t*, const resp_t*, resp_t**, int);
int redis_remove(const resp_t*);
extern void redis_server_run(int);

#endif
