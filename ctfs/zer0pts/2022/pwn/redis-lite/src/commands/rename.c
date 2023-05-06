#include <stdlib.h>
#include "commands.h"

resp_t* __redis_run_RENAME(const resp_array_t* argv) {
  resp_t *src, *dst;
  redis_db_t *item;

  if (argv->count != 3)
    return resp_new_error("ERR wrong number of arguments for 'rename' command");

  src = argv->elements[1];
  dst = argv->elements[2];
  if (resp_equals(src, dst))
    return resp_new_integer(0);

  /* Retrieve item at key */
  if ((item = redis_get(src)) == NULL)
    return resp_new_error("ERR no such key");

  /* Move key */
  resp_release_data(item->key);
  item->key = resp_copy(dst);

  return resp_new_message("OK");
}

resp_t* __redis_help_RENAME(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("rename", 6);
  // Arity
  data->array.elements[1] = resp_new_integer(3);
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
