#include "commands.h"

resp_t* __redis_run_TYPE(const resp_array_t* argv) {
  redis_db_t *item;

  if (argv->count != 2)
    return resp_new_error("ERR wrong number of arguments for 'type' command");

  /* Retrieve item at key */
  if ((item = redis_get(argv->elements[1])) == NULL)
    return resp_new_string("none", 4);

  switch (item->value->type) {
    case RESP_TYPE_INTEGER:
      return resp_new_string("integer", 7);
    case RESP_TYPE_MESSAGE:
    case RESP_TYPE_ERROR:
    case RESP_TYPE_STRING:
      return resp_new_string("string", 6);
    case RESP_TYPE_ARRAY:
      return resp_new_string("list", 4);
  }

  return resp_new_string("none", 4);
}

resp_t* __redis_help_TYPE(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("type", 4);
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
