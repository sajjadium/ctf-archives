#ifndef __COMMANDS_HEADER__
#define __COMMANDS_HEADER__

#include "../redis.h"
#include "../resp.h"

resp_t* __redis_run_COMMAND(const resp_array_t*);
resp_t* __redis_help_COMMAND(void);

resp_t* __redis_run_COPY(const resp_array_t*);
resp_t* __redis_help_COPY(void);

resp_t* __redis_run_DEL(const resp_array_t*);
resp_t* __redis_help_DEL(void);

resp_t* __redis_run_ECHO(const resp_array_t*);
resp_t* __redis_help_ECHO(void);

resp_t* __redis_run_EXISTS(const resp_array_t*);
resp_t* __redis_help_EXISTS(void);

resp_t* __redis_run_FLUSHALL(const resp_array_t*);
resp_t* __redis_help_FLUSHALL(void);

resp_t* __redis_run_GET(const resp_array_t*);
resp_t* __redis_help_GET(void);

resp_t* __redis_run_MGET(const resp_array_t*);
resp_t* __redis_help_MGET(void);

resp_t* __redis_run_MSET(const resp_array_t*);
resp_t* __redis_help_MSET(void);

resp_t* __redis_run_RENAME(const resp_array_t*);
resp_t* __redis_help_RENAME(void);

resp_t* __redis_run_SET(const resp_array_t*);
resp_t* __redis_help_SET(void);

resp_t* __redis_run_SETNX(const resp_array_t*);
resp_t* __redis_help_SETNX(void);

resp_t* __redis_run_TYPE(const resp_array_t*);
resp_t* __redis_help_TYPE(void);

#endif
