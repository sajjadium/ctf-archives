#include "commands.h"

resp_t* __redis_run_EXISTS(const resp_array_t* argv) {
  if (argv->count != 2)
    return resp_new_error("ERR wrong number of arguments for 'exists' command");

  /* Retrieve item at key */
  if (redis_get(argv->elements[1]) == NULL)
    return resp_new_integer(0);

  return resp_new_integer(1);
}

resp_t* __redis_help_EXISTS(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("exists", 6);
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
