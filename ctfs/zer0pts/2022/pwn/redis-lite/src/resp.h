#ifndef __RESP_HEADER__
#define __RESP_HEADER__

#include <stddef.h>

#define RESP_STRING_CAPACITY 0x10

/* Data types */
typedef enum {
  RESP_TYPE_MESSAGE,
  RESP_TYPE_ERROR,
  RESP_TYPE_INTEGER,
  RESP_TYPE_STRING,
  RESP_TYPE_ARRAY,
} RESP_TYPE;

typedef RESP_TYPE resp_type_t;

struct resp_t;

/* Definition of types */
typedef struct {
  int size;
  char *data;
} resp_string_t;
typedef resp_string_t resp_message_t;
typedef resp_string_t resp_error_t;
typedef int resp_integer_t;
typedef struct resp_array_t {
  int count;
  struct resp_t **elements;
} resp_array_t;

/* Structure of data */
typedef struct resp_t {
  resp_type_t type;
  union {
    resp_message_t message;
    resp_error_t error;
    resp_integer_t integer;
    resp_string_t string;
    resp_array_t array;
  };
} resp_t;

/* Function prototype */
resp_t *resp_receive_data(int);
int resp_send_data(int, const resp_t*);
int resp_equals(const resp_t *a, const resp_t *b);
resp_t* resp_copy(const resp_t *old);
resp_t* resp_new_message(const char*);
resp_t* resp_new_error(const char*);
resp_t* resp_new_string(const char*, int len);
resp_t* resp_new_integer(int v);
resp_t* resp_new_array(size_t n);
void resp_release_data(resp_t*);

#endif
