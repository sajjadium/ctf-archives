#include <malloc.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "resp.h"

#define WRITE(fd, data, size) \
  if (write(fd, data, size) < 0) goto ERROR;

/**
 * Receive exactly @p len bytes from @p fd.
 * @brief Receive a byte array
 * @param (fd) File descriptor to read data from
 * @param (buf) Pointer to the buffer to store data
 * @param (len) Length to read
 * @return Returns the size of received data on success, -1 on error
 */
ssize_t __resp_receive(int fd, char *buf, size_t len) {
  size_t size;

  for (size = 0; size < len; size++) {
    if (read(fd, &buf[size], 1) != 1)
      return -1;
  }

  return size;
}

/**
 * Receive a line of string.
 * @brief Receive a line of string
 * @param (fd) File descriptor to read data from
 * @param (pdata) Pointer of pointer to the buffer to store data
 * @param (capacity) Current capacity of the buffer
 * @return Returns the size of received data on success, -1 on error
 */
size_t __receive_line(int fd, char **pdata, size_t capacity) {
  char c;
  size_t size = 0;

  while(1) {
    /* Read a byte */
    if (__resp_receive(fd, &c, 1) != 1)
      goto ERROR;

    /* Check the end of line ("\r\n") */
    if ((size > 0)
        && (c == '\n')
        && ((*pdata)[size-1] == '\r')) {
      (*pdata)[--size] = '\0';
      break;
    }

    /* Store a byte */
    (*pdata)[size] = c;

    /* Expand buffer if the capacity is insufficient */
    if (++size >= capacity) {
      capacity *= 2;
      if ((*pdata = realloc(*pdata, capacity)) == NULL)
        return -1;
    }
  }

  return size;

 ERROR:
  free(*pdata);
  return -1;
}

/**
 * Receive an integer value.
 * @brief Receive an integer
 * @param (fd) File descriptor to receive data from
 * @param (value) Pointer to integer field to store the result
 * @return 0 on success, 1 on error
 */
int __receive_integer(int fd, int *value) {
  char *endptr;
  char *str_value;

  /* Receive a line of string */
  if ((str_value = malloc(RESP_STRING_CAPACITY)) == NULL)
    return 1;
  if (__receive_line(fd, &str_value, RESP_STRING_CAPACITY) < 0)
    return 1;

  /* Convert into integer */
  *value = strtol(str_value, &endptr, 10);
  if (*endptr == '\0') {
    free(str_value); // We must free this variable after the comparison
                     // as `endptr` is a part of `str_value`
    return 0;
  } else {
    free(str_value);
    return 1;
  }
}

/**
 * Receive a RESP message or error.
 * @brief Receive a RESP-represented string
 * @param (fd) File descriptor to receive data from
 * @param (data) RESP struct to store data
 * @return 0 on success, 1 on error
 */
int resp_receive_line(int fd, resp_t *data) {
  if ((data->message.data = malloc(RESP_STRING_CAPACITY)) == NULL)
    return 1;

  data->message.size
    = __receive_line(fd, &data->message.data, RESP_STRING_CAPACITY);
  if (data->message.size < 0)
    return 1;

  return 0;
}

/**
 * Receive a RESP integer.
 * @brief Receive a RESP-represented integer
 * @param (fd) File descriptor to receive data from
 * @param (data) RESP struct to store data
 * @return 0 on success, 1 on error
 */
int resp_receive_integer(int fd, resp_t *data) {
  if (__receive_integer(fd, &data->integer))
    return 1;
  else
    return 0;
}

/**
 * Receive a Bulk String.
 * @brief Receive a RESP-represented string
 * @param (fd) File descriptor to receive data from
 * @param (data) RESP struct to store data
 * @return 0 on success, 1 on error
 */
int resp_receive_bulk(int fd, resp_t *data) {
  int capacity;
  char endline[2];

  /* Get the size of data */
  if (__receive_integer(fd, &data->string.size))
    return 1;

  if (data->string.size == -1) { /* Null */

    if (__resp_receive(fd, endline, 2) != 2)
      return 1;
    if (endline[0] != '\r' || endline[1] != '\n')
      return 1;

    data->string.data = NULL;
    return 0;

  } else { /* Bulk String */
    capacity = data->string.size + 3;
    if ((data->string.data = calloc(1, capacity)) == NULL)
      return 1;

    if (__resp_receive(fd, data->string.data, data->string.size + 2) < 0)
      goto ERROR;

    if (data->string.data[data->string.size] != '\r'
        || data->string.data[data->string.size+1] != '\n')
      goto ERROR;

    data->string.data[data->string.size] = '\0';
    return 0;
  }

 ERROR:
  free(data->string.data);
  return 1;
}

/**
 * Receive a RESP array.
 * @brief Receive a RESP-represented array
 * @param (fd) File descriptor to receive data from
 * @param (data) RESP struct to store data
 * @return 0 on success, 1 on error
 */
int resp_receive_array(int fd, resp_t *data) {
  int i, j;

  /* Get the number of elements */
  if (__receive_integer(fd, &data->array.count))
    return 1;

  data->array.elements
    = (resp_t**)calloc(sizeof(resp_t*), data->array.count);
  if (data->array.elements == NULL)
    return 1;

  /* Read each element */
  for (i = 0; i < data->array.count; i++) {
    data->array.elements[i] = resp_receive_data(fd);
    if (data->array.elements[i] == NULL) {
      /* On failure, release every element received so far */
      for (j = 0; j < i; j++) {
        resp_release_data(data->array.elements[j]);
      }
      free(data->array.elements);
      return 1;
    }
  }

  return 0;
}

/**
 * Receive a RESP data from the client.
 * @brief Receive a RESP data
 * @param (fd) File descriptor to receive data from
 * @return Returns a pointer to resp_t structure on success, otherwise NULL
 */
resp_t *resp_receive_data(int fd) {
  char c;
  resp_t *data;

  if ((data = (resp_t*)calloc(sizeof(resp_t), 1)) == NULL)
    return NULL;

  /* Receive the type */
  if (__resp_receive(fd, &c, 1) != 1) goto ERROR;

  switch(c) {
    case '+': /* Message type */
      data->type = RESP_TYPE_MESSAGE;
      if (resp_receive_line(fd, data)) goto ERROR;
      break;

    case '-': /* Error type */
      data->type = RESP_TYPE_ERROR;
      if (resp_receive_line(fd, data)) goto ERROR;
      break;

    case ':': /* Integer type */
      data->type = RESP_TYPE_INTEGER;
      if (resp_receive_integer(fd, data)) goto ERROR;
      break;

    case '$': /* Bulk string type */
      data->type = RESP_TYPE_STRING;
      if (resp_receive_bulk(fd, data)) goto ERROR;
      break;

    case '*': /* Array type */
      data->type = RESP_TYPE_ARRAY;
      if (resp_receive_array(fd, data)) goto ERROR;
      break;

    default:
      goto ERROR;
  }

  return data;

 ERROR:
  free(data);
  return NULL;
}

/**
 * Send a RESP data to the client.
 * @brief Send a RESP data
 * @param (fd) File descriptor to send data to
 * @param (data) RESP structure to send
 * @return 0 if successful, 1 on failure
 */
int resp_send_data(int fd, const resp_t* data) {
  int i, n;
  char buf[0x10];

  if (data == NULL) {
    WRITE(fd, "-ERR internal server error\r\n", 28);
    goto ERROR;
  }

  switch (data->type) {
    case RESP_TYPE_MESSAGE: 
      WRITE(fd, "+", 1);
      WRITE(fd, data->message.data, data->message.size);
      WRITE(fd, "\r\n", 2);
      break;

    case RESP_TYPE_ERROR:
      WRITE(fd, "-", 1);
      WRITE(fd, data->error.data, data->error.size);
      WRITE(fd, "\r\n", 2);
      break;

    case RESP_TYPE_STRING:
      n = snprintf(buf, sizeof(buf), "%d", data->string.size);
      WRITE(fd, "$", 1);
      WRITE(fd, buf, n);
      WRITE(fd, "\r\n", 2);
      if (data->string.size >= 0) {
        WRITE(fd, data->string.data, data->string.size);
        WRITE(fd, "\r\n", 2);
      }
      break;

    case RESP_TYPE_INTEGER:
      n = snprintf(buf, sizeof(buf), "%d", data->integer);
      WRITE(fd, ":", 1);
      WRITE(fd, buf, n);
      WRITE(fd, "\r\n", 2);
      break;

    case RESP_TYPE_ARRAY:
      n = snprintf(buf, sizeof(buf), "%d", data->array.count);
      WRITE(fd, "*", 1);
      WRITE(fd, buf, n);
      WRITE(fd, "\r\n", 2);
      for (i = 0; i < data->array.count; i++) {
        if (resp_send_data(fd, data->array.elements[i]))
          return 1;
      }
      break;

    default:
      WRITE(fd, "-ERR internal server error\r\n", 28);
      goto ERROR;
  }

  return 0;

 ERROR:
  return 1;
}

/**
 * Create a new RESP string.
 * @brief Create a new string
 * @param (s) Pointer to string
 * @param (len) Size of string
 * @param (type) Type (message, error, or string)
 */
resp_t* __resp_internal_new_string(const char *s, int len, RESP_TYPE type) {
  resp_t *data;

  if ((data = (resp_t*)calloc(sizeof(resp_t), 1)) == NULL)
    return NULL;

  data->type = type;
  if (s) {
    data->string.data = strndup(s, len);
    data->string.size = len;

  } else if (type == RESP_TYPE_STRING) {
    data->string.data = NULL;
    data->string.size = -1;

  } else {
    free(data);
    return NULL;
  }

  return data;
}

/**
 * Check if two RESP structures represent the same value.
 * @brief Compare two RESP structures.
 * @param (a) First value
 * @param (b) Second value to compare with @p a
 * @return 1 if two values are equivalent, otherwise 0
 */
int resp_equals(const resp_t *a, const resp_t *b) {
  int i;

  /* If type is different, always return false */
  if (a->type != b->type)
    return 0;

  /* Check is different for each type */
  switch (a->type) {
    case RESP_TYPE_MESSAGE: // String
    case RESP_TYPE_ERROR:
    case RESP_TYPE_STRING:
      if (a->string.size != b->string.size)
        return 0;

      if (a->string.size == -1) {
        return 1;
      } else {
        return memcmp(a->string.data, b->string.data, a->string.size) == 0;
      }

    case RESP_TYPE_INTEGER: // Integer
      return a->integer == b->integer;

    case RESP_TYPE_ARRAY: // Array
      if (a->array.count != b->array.count)
        return 0;

      for (i = 0; i < a->array.count; i++) {
        if (resp_equals(a->array.elements[i], b->array.elements[i]))
          return 0;
      }
      return 1;

    default: // Invalid type
      return 0;
  }
}

/**
 * Create a deep copy of a RESP object.
 * @brief Duplicate a RESP object
 * @param (o) Object to copy
 * @return Pointer to the copied RESP structure
 */
resp_t* resp_copy(const resp_t *old) {
  int i, j;
  resp_t *new;

  if ((new = (resp_t*)calloc(sizeof(resp_t), 1)) == NULL)
    return NULL;

  new->type = old->type;
  switch (new->type) {
    case RESP_TYPE_MESSAGE: // String
    case RESP_TYPE_ERROR:
    case RESP_TYPE_STRING:
      new->string.size = old->string.size;
      if (new->string.size == -1)
        break;

      new->string.data = (char*)malloc(new->string.size);
      if (new->string.data == NULL) {
        free(new);
        return NULL;
      }

      memcpy(new->string.data, old->string.data, new->string.size);
      break;

    case RESP_TYPE_INTEGER: // Integer
      new->integer = old->integer;
      break;

    case RESP_TYPE_ARRAY: // Array
      new->array.count = old->array.count;
      new->array.elements = (resp_t**)calloc(sizeof(resp_t*), new->array.count);
      if (new->array.elements == NULL) {
        free(new);
        return NULL;
      }

      for (i = 0; i < new->array.count; i++) {
        new->array.elements[i] = resp_copy(old->array.elements[i]);
        if (new->array.elements[i] == NULL) {
          /* On failure, release every element created so far */
          for (j = 0; j < i; j++) {
            resp_release_data(new->array.elements[j]);
          }
          free(new->array.elements);
          free(new);
          return NULL;
        }
      }
      break;

    default: // Invalid type
      return NULL;
  }

  return new;
}

/**
 * Create a new RESP message string.
 * @brief Create a new RESP message
 * @param (s) Pointer to string
 * @return Created object
 */
resp_t* resp_new_message(const char *s) {
  return __resp_internal_new_string(s, strlen(s), RESP_TYPE_MESSAGE);
}

/**
 * Create a new RESP error string.
 * @brief Create a new RESP error
 * @param (s) Pointer to string
 * @return Created object
 */
resp_t* resp_new_error(const char *s) {
  return __resp_internal_new_string(s, strlen(s), RESP_TYPE_ERROR);
}

/**
 * Create a new Bulk String.
 * @brief Create a new RESP string
 * @param (s) Pointer to string
 * @param (len) Size of string (-1 if null)
 * @return Created object
 */
resp_t* resp_new_string(const char *s, int len) {
  return __resp_internal_new_string(s, len, RESP_TYPE_STRING);
}

/**
 * Create a new RESP integer.
 * @brief Create a new RESP integer
 * @param (s) Value
 * @return Created object
 */
resp_t* resp_new_integer(int v) {
  resp_t *data;

  if ((data = (resp_t*)calloc(sizeof(resp_t), 1)) == NULL)
    return NULL;

  data->type = RESP_TYPE_INTEGER;
  data->integer = v;
  return data;
}

/**
 * Create a new RESP array with empty elements.
 * @brief Create a new RESP array
 * @param (n) Size of array
 * @return Created object
 */
resp_t* resp_new_array(size_t n) {
  resp_t *data;

  if ((data = (resp_t*)calloc(sizeof(resp_t), 1)) == NULL)
    return NULL;

  data->type = RESP_TYPE_ARRAY;
  data->array.count = n;
  data->array.elements = (resp_t**)calloc(sizeof(resp_t*), n);
  if (data->array.elements == NULL) {
    free(data);
    return NULL;
  }

  return data;
}

/**
 * Release a RESP object.
 * @brief Release a RESP object
 * @param (data) RESP structure to free
 */
void resp_release_data(resp_t *data) {
  int i;

  if (data == NULL)
    return;

  switch(data->type) {

    /* If this is an array, release every element */
    case RESP_TYPE_ARRAY:
      for (i = 0; i < data->array.count; i++)
        resp_release_data(data->array.elements[i]);
      free(data->array.elements);
      break;

    /* For message, error, and bulk string types, release the data */
    case RESP_TYPE_MESSAGE:
    case RESP_TYPE_ERROR:
    case RESP_TYPE_STRING:
      free(data->string.data);
      break;

    default:
      break;
  }

  free(data);
}
