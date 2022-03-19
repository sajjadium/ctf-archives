#include <stdlib.h>
#include <string.h>
#include "commands.h"

resp_t* __redis_run_COMMAND(const resp_array_t* argv) {
  int i, j;
  resp_t *data;

  if (argv->count > 2)
    return resp_new_error("ERR wrong number of arguments for 'command' command");

  if (argv->count == 1) {
    /* Return every command */
    if ((data = resp_new_array(redis_cmd_count)) == NULL)
      return NULL;

    for (i = 0; i < redis_cmd_count; i++) {
      /* Get usage for each command */
      data->array.elements[i] = redis_cmd_list[i].help();

      if (data->array.elements[i] == NULL) {
        /* On failure, release every element created so far */
        for (j = 0; j < i; j++) {
          resp_release_data(data->array.elements[j]);
        }
        free(data->array.elements);
        free(data);
        return NULL;
      }
    }

    return data;

  } else if (argv->count == 2
             && argv->elements[1]->type == RESP_TYPE_STRING
             && strcasecmp(argv->elements[1]->string.data, "COUNT") == 0) {
    return resp_new_integer(redis_cmd_count);

  } else {
    return resp_new_error("ERR syntax error");
  }
}

resp_t* __redis_help_COMMAND(void) {
  resp_t *data;

  if ((data = resp_new_array(6)) == NULL)
    return NULL;

  // Name
  data->array.elements[0] = resp_new_string("command", 7);
  // Arity
  data->array.elements[1] = resp_new_integer(-1);
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
