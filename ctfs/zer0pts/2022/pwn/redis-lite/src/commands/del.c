#include "commands.h"

resp_t* __redis_run_DEL(const resp_array_t* argv) {
  int i, num_deleted;

  if (argv->count < 2)
    return resp_new_error("ERR wrong number of arguments for 'del' command");

  num_deleted = 0;
  for (i = 1; i < argv->count; i++) {
    num_deleted += redis_remove(argv->elements[i]);
  }

  return resp_new_integer(num_deleted);
}

resp_t* __redis_help_DEL(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("del", 3);
  // Arity
  data->array.elements[1] = resp_new_integer(-2);
  // Flags
  data->array.elements[2] = resp_new_array(1);
  data->array.elements[2]->array.elements[0] = resp_new_string("write", 5);
  // First key
  data->array.elements[3] = resp_new_integer(1);
  // Last key
  data->array.elements[4] = resp_new_integer(-1);
  // Step
  data->array.elements[5] = resp_new_integer(1);

  return data;
}

