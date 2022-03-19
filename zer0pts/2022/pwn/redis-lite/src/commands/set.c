#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "commands.h"

typedef struct {
  int (*fn_sleep)(unsigned int);
  int unit;
  int timeout;
  resp_t *key;
} expiration_t;

void *expiration_handler(void *arg) {
  int i;
  const expiration_t* config = (expiration_t*)arg;

  for (i = 0; i < config->timeout; i++) {
    /* Use loop to avoid integer overflow on usleep timeout */
    config->fn_sleep(config->unit);
  }
  redis_remove(config->key);

  resp_release_data(config->key);
  free(arg);
  return NULL;
}

resp_t* __redis_run_SET(const resp_array_t* argv) {
  int r, timeout;
  char *endptr;
  const resp_t *key, *value;
  resp_t *old;
  pthread_t th;
  expiration_t *config;

  if (argv->count < 3)
    return resp_new_error("ERR wrong number of arguments for 'set' command");

  key   = argv->elements[1];
  value = argv->elements[2];

  config = NULL;
  if (argv->count >= 4) {
    if (argv->count == 5
        && argv->elements[3]->type == RESP_TYPE_STRING
        && (argv->elements[4]->type == RESP_TYPE_STRING
            || argv->elements[4]->type == RESP_TYPE_INTEGER)) {
      /* Set expiration */
      endptr = NULL;
      timeout = argv->elements[4]->type == RESP_TYPE_INTEGER
        ? argv->elements[4]->integer
        : strtol(argv->elements[4]->string.data, &endptr, 10);

      if ((endptr && *endptr != '\0') || timeout <= 0)
        return resp_new_error("ERR invalid expire time in set");

      if (strcasecmp(argv->elements[3]->string.data, "EX") == 0) {
        /* Seconds */
        if ((config = (expiration_t*)malloc(sizeof(expiration_t))) == NULL)
          return NULL;

        config->fn_sleep = (int (*)(unsigned))sleep;
        config->unit     = 1;
        config->timeout  = timeout;

      } else if (strcasecmp(argv->elements[3]->string.data, "PX") == 0) {
        /* Milliseconds */
        if ((config = (expiration_t*)malloc(sizeof(expiration_t))) == NULL)
          return NULL;

        config->fn_sleep = usleep;
        config->unit     = 1000;
        config->timeout  = timeout;

      } else {
        return resp_new_error("ERR syntax error");
      }

    } else {
      return resp_new_error("ERR syntax error");
    }
  }

  r = redis_insert(key, value, &old, 1);
  if (r != -1 && config) {
    /* Create thread to expire key */
    if ((config->key = resp_copy(key)) == NULL) {
      free(config);
      return NULL;
    }

    if (pthread_create(&th, NULL, expiration_handler, (void*)config)) {
      resp_release_data(config->key);
      free(config);
      return NULL;
    }

    if (pthread_detach(th))
      return NULL;
  }

  if (r == -1) {
    /* Failure */
    return NULL;

  } else if (r == 0) {
    /* Successful */
    return resp_new_message("OK");

  } else {
    /* Return old value if item already exists */
    return old;
  }
}

resp_t* __redis_run_MSET(const resp_array_t* argv) {
  int i, r, num_set;
  resp_t *old;

  if (argv->count < 2 || (argv->count - 1) % 2 != 0)
    return resp_new_error("ERR wrong number of arguments for 'mset' command");

  /* Set items at each key */
  num_set = 0;
  for (i = 0; i < (argv->count - 1) / 2; i++) {
    r = redis_insert(argv->elements[1+i*2], argv->elements[i*2+2], &old, 1);
    if (r == -1) {
      /* Failure */
      return NULL;

    } else if (r >= 0) {
      /* Successful */
      num_set++;

    }
  }

  return resp_new_integer(num_set);
}

resp_t* __redis_run_SETNX(const resp_array_t* argv) {
  int r;
  const resp_t *key, *value;
  resp_t *old;

  if (argv->count != 3)
    return resp_new_error("ERR wrong number of arguments for 'setnx' command");

  key   = argv->elements[1];
  value = argv->elements[2];
  r = redis_insert(key, value, &old, 0);
  if (r == -1) {
    /* Failure */
    return NULL;

  } else if (r == 0) {
    /* Return 1 if successful */
    return resp_new_integer(1);

  } else {
    /* Return 0 if item already exists */
    return resp_new_integer(0);
  }
}

resp_t* __redis_help_SET(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("set", 3);
  // Arity
  data->array.elements[1] = resp_new_integer(-3);
  // Flags
  data->array.elements[2] = resp_new_array(2);
  data->array.elements[2]->array.elements[0] = resp_new_string("write", 5);
  data->array.elements[2]->array.elements[1] = resp_new_string("denyoom", 7);
  // First key
  data->array.elements[3] = resp_new_integer(1);
  // Last key
  data->array.elements[4] = resp_new_integer(1);
  // Step
  data->array.elements[5] = resp_new_integer(1);

  return data;
}

resp_t* __redis_help_MSET(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("mset", 4);
  // Arity
  data->array.elements[1] = resp_new_integer(-2);
  // Flags
  data->array.elements[2] = resp_new_array(2);
  data->array.elements[2]->array.elements[0] = resp_new_string("write", 5);
  data->array.elements[2]->array.elements[1] = resp_new_string("denyoom", 7);
  // First key
  data->array.elements[3] = resp_new_integer(1);
  // Last key
  data->array.elements[4] = resp_new_integer(-1);
  // Step
  data->array.elements[5] = resp_new_integer(2);

  return data;
}

resp_t* __redis_help_SETNX(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("setnx", 5);
  // Arity
  data->array.elements[1] = resp_new_integer(-3);
  // Flags
  data->array.elements[2] = resp_new_array(2);
  data->array.elements[2]->array.elements[0] = resp_new_string("write", 5);
  data->array.elements[2]->array.elements[1] = resp_new_string("denyoom", 7);
  // First key
  data->array.elements[3] = resp_new_integer(1);
  // Last key
  data->array.elements[4] = resp_new_integer(1);
  // Step
  data->array.elements[5] = resp_new_integer(1);

  return data;
}
