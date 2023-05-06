#include <pthread.h>
#include <string.h>
#include <stdlib.h>
#include "redis.h"
#include "commands/commands.h"

int redis_cmd_count;
redis_command_t redis_cmd_list[] =
  {
   {"COMMAND", __redis_run_COMMAND, __redis_help_COMMAND},
   {"ECHO", __redis_run_ECHO, __redis_help_ECHO},
   {"GET", __redis_run_GET, __redis_help_GET},
   {"MGET", __redis_run_MGET, __redis_help_MGET},
   {"SET", __redis_run_SET, __redis_help_SET},
   {"MSET", __redis_run_MSET, __redis_help_MSET},
   {"SETNX", __redis_run_SETNX, __redis_help_SETNX},
   {"DEL", __redis_run_DEL, __redis_help_DEL},
   {"COPY", __redis_run_COPY, __redis_help_COPY},
   {"EXISTS", __redis_run_EXISTS, __redis_help_EXISTS},
   {"RENAME", __redis_run_RENAME, __redis_help_RENAME},
   {"TYPE", __redis_run_TYPE, __redis_help_TYPE},
   {"FLUSHALL", __redis_run_FLUSHALL, __redis_help_FLUSHALL},
   {NULL, NULL, NULL}
  };

pthread_mutex_t redis_db_mutex;
redis_db_t *redis_db = NULL;

/**
 * Release an item including its key and value.
 * @brief Release an item
 */
void redis_release_item(redis_db_t *item) {
  resp_release_data(item->key);
  resp_release_data(item->value);
  free(item);
}

/**
 * Delete all the keys registered in the database.
 * @brief Delete all the keys
 */
void redis_clear() {
  redis_db_t *cur, *old;

  pthread_mutex_lock(&redis_db_mutex);

  cur = redis_db;
  while (cur) {
    old = cur;
    cur = cur->next;
    redis_release_item(old);
  }

  redis_db = NULL;

  pthread_mutex_unlock(&redis_db_mutex);
}

/**
 * Find an item from the database if it exists.
 * @brief Lookup redis DB for a key
 * @param (key) RESP-represented key
 * @return Returns an item if it's found, otherwise returns NULL
 */
redis_db_t* redis_get(const resp_t* key) {
  redis_db_t *cur;

  pthread_mutex_lock(&redis_db_mutex);

  for (cur = redis_db; cur; cur = cur->next) {
    if (resp_equals(cur->key, key)) {
      /* Found */
      pthread_mutex_unlock(&redis_db_mutex);
      return cur;
    }
  }

  /* Not found */
  pthread_mutex_unlock(&redis_db_mutex);
  return NULL;
}

/**
 * Insert a new item to the database.
 * @brief Insert a new item
 * @param (key) Key of the item
 * @param (value) Value of the item
 * @param (old) Pointer to RESP structure to store the old value into
 * @param (overwrite) Overwrite value when key exists if this value is not zero
 * @return -1 on failure, 0 if successful, and 1 if item already exists
 */
int redis_insert(const resp_t *key, const resp_t *value,
                 resp_t **old, int overwrite) {
  redis_db_t *item;

  if (item = redis_get(key)) {
    /* Key exists */
    if (overwrite) {
      /* Update value only if `overwrite` is non-zero */
      pthread_mutex_lock(&redis_db_mutex);

      if (old) {
        /* This value must be freed by the caller */
        *old = item->value;
      } else {
        /* If the caller doesn't receive the old value, we free it instead */
        free(item->value);
      }

      item->value = resp_copy(value);

      pthread_mutex_unlock(&redis_db_mutex);
    }
    return 1;

  } else {
    /* Insert */
    item = (redis_db_t*)malloc(sizeof(redis_db_t));
    if (item == NULL)
      return -1;

    item->key = resp_copy(key);
    item->value = resp_copy(value);

    pthread_mutex_lock(&redis_db_mutex);

    if (redis_db == NULL) {
      /* First item to insert */
      item->next = NULL;
      item->prev = NULL;

    } else {
      /* Link to list */
      item->next = redis_db;
      item->prev = NULL;
      redis_db->prev = item;
    }

    redis_db = item;
    pthread_mutex_unlock(&redis_db_mutex);

    return 0;
  }
}

/**
 * Remove and unlink an item at a specific key.
 * @brief Remove an item at a key
 * @param (key) Key of the item to remove
 * @return Number of items deleted (0 or 1)
 */
int redis_remove(const resp_t* key) {
  redis_db_t *item;

  if (item = redis_get(key)) {
    /* Unlink */
    pthread_mutex_lock(&redis_db_mutex);

    if (item == redis_db) {
      /* Top item */
      redis_db = item->next;
      if (item->next)
        item->next->prev = item->prev;

    } else {
      /* Not the top item */
      item->prev->next = item->next;
      if (item->next)
        item->next->prev = item->prev;
    }

    pthread_mutex_unlock(&redis_db_mutex);

    /* Release */
    redis_release_item(item);

    return 1;
  }

  return 0;
}

/**
 * Parses a RESP-resresented array and run a command.
 * @brief Run a command
 * @param (argv) Arguments of the command
 * @return Result of the command
 */
resp_t* redis_run_command(const resp_array_t* argv) {
  int i;
  resp_t *data;

  /* Invalid command name */
  if (argv->elements[0]->type != RESP_TYPE_STRING
      || argv->elements[0]->string.size == -1)
    return NULL;

  for (i = 0; i < redis_cmd_count; i++) {
    if (strcasecmp(redis_cmd_list[i].name,
                   argv->elements[0]->string.data) == 0) {
      /* Run matching command */
      if (data = redis_cmd_list[i].run(argv))
        return data;

      return resp_new_error("ERR internal error");
    }
  }

  /* Command not found */
  return resp_new_error("ERR unknown command");
}

/**
 * Receive and run Redis commands forever.
 * @brief Server main
 * @param (fd) File descriptor to receive commands from and send results to
 */
void redis_server_run(int fd) {
  resp_t *data, *result;

  /* Calculate the number of commands */
  for (redis_cmd_count = 0;
       redis_cmd_list[redis_cmd_count].name;
       redis_cmd_count++);

  pthread_mutex_init(&redis_db_mutex, NULL);

  while(1) {
    /* Receive a command */
    if ((data = resp_receive_data(fd)) == NULL)
      break;

    /* Command must be a non-empty array */
    if (data->type != RESP_TYPE_ARRAY
        || data->array.count <= 0) {
      resp_release_data(data);
      break;
    }

    /* Run command */
    result = redis_run_command(&data->array);
    resp_release_data(data);

    /* Send result */
    resp_send_data(fd, result);
    resp_release_data(result);
  }
}
