#include "commands.h"

resp_t* __redis_run_FLUSHALL(const resp_array_t* argv) {
  if (argv->count != 1)
    return resp_new_error("ERR wrong number of arguments for 'flushall' command");

  redis_clear();

  return resp_new_message("OK");
}

resp_t* __redis_help_FLUSHALL(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("flushall", 8);
  // Arity
  data->array.elements[1] = resp_new_integer(1);
  // Flags
  data->array.elements[2] = resp_new_array(1);
  data->array.elements[2]->array.elements[0] = resp_new_string("write", 5);
  // First key
  data->array.elements[3] = resp_new_integer(1);
  // Last key
  data->array.elements[4] = resp_new_integer(1);
  // Step
  data->array.elements[5] = resp_new_integer(1);

  return data;
}
