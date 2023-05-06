#include <stdlib.h>
#include "commands.h"

resp_t* __redis_run_GET(const resp_array_t* argv) {
  const redis_db_t *item;

  if (argv->count != 2)
    return resp_new_error("ERR wrong number of arguments for 'get' command");

  /* Retrieve item at key */
  if ((item = redis_get(argv->elements[1])) == NULL)
    return resp_new_string(NULL, 0);

  return resp_copy(item->value);
}

resp_t* __redis_run_MGET(const resp_array_t* argv) {
  int i, j;
  const redis_db_t *item;

  if (argv->count < 2)
    return resp_new_error("ERR wrong number of arguments for 'mget' command");

  resp_t *res = resp_new_array(argv->count - 1);
  if (res == NULL)
    return NULL;

  /* Retrieve items at each key */
  for (i = 0; i < res->array.count; i++) {
    if (item = redis_get(argv->elements[i+1])) {
      /* Item found */
      res->array.elements[i] = resp_copy(item->value);

    } else {
      /* Item not found */
      res->array.elements[i] = resp_new_string(NULL, 0);
    }

    if (res->array.elements[i] == NULL) {
      /* On failure, release every element created so far */
      for (j = 0; j < i; j++) {
        resp_release_data(res->array.elements[j]);
      }
      free(res->array.elements);
      free(res);
      return NULL;
    }
  }

  return res;
}

resp_t* __redis_help_GET(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("get", 3);
  // Arity
  data->array.elements[1] = resp_new_integer(2);
  // Flags
  data->array.elements[2] = resp_new_array(1);
  data->array.elements[2]->array.elements[0] = resp_new_string("readonly", 8);
  // First key
  data->array.elements[3] = resp_new_integer(1);
  // Last key
  data->array.elements[4] = resp_new_integer(1);
  // Step
  data->array.elements[5] = resp_new_integer(1);

  return data;
}

resp_t* __redis_help_MGET(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("mget", 4);
  // Arity
  data->array.elements[1] = resp_new_integer(-2);
  // Flags
  data->array.elements[2] = resp_new_array(1);
  data->array.elements[2]->array.elements[0] = resp_new_string("readonly", 8);
  // First key
  data->array.elements[3] = resp_new_integer(1);
  // Last key
  data->array.elements[4] = resp_new_integer(-1);
  // Step
  data->array.elements[5] = resp_new_integer(1);

  return data;
}
