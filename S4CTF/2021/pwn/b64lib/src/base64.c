#include "base64.h"

int __b64_error;

/* Base64 table */
static const char b64_table[64] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
char b64_reverse_table[256] = {0};

__attribute__((constructor))
void __b64_init_reverse_table(void) {
  int i, j;

  /* Create reverse table */
  for(i = 0; i < 0x100; i++) {
    char c = -1;
    for(j = 0; j < 64; j++) {
      if (b64_table[j] == (char)i) {
        c = (char)j;
        break;
      }
    }
    b64_reverse_table[i] = c;
  }
  b64_reverse_table[0x3d] = 0; // '='
}

/**
 * b64encode: Encode input string to base64
 */
void b64encode(const char *input, char *output, int size) {
  int i, j;
  unsigned int block;
  unsigned int masks[] = {0, 0xfff000, 0xffffc0};
  __b64_error = B64_ERROR_NONE;

  /* Encode */
  for(i = j = 0; i < size - 2; i += 3, j += 4) {
    block = (input[i] << 16) | (input[i+1] << 8) | input[i+2];
    output[j+0] = b64_table[block >> 18];
    output[j+1] = b64_table[(block >> 12) & 0b111111];
    output[j+2] = b64_table[(block >> 6) & 0b111111];
    output[j+3] = b64_table[block & 0b111111];
  }

  /* Encode padding block if necessary */
  if (size % 3) {
    block = (input[i] << 16) | (input[i+1] << 8) | input[i+2];
    block &= masks[size % 3];
    output[j+0] = b64_table[(block >> 18) & 0b111111];
    output[j+1] = b64_table[(block >> 12) & 0b111111];
    if (size % 3 == 2)
      output[j+2] = b64_table[(block >> 6) & 0b111111];
    else
      output[j+2] = '=';
    output[j+3] = '=';
    j += 4;
  }

  /* Null terminate */
  output[j] = 0;
}

/**
 * b64decode: Decode input string as base64
 */
void b64decode(const char *input, char *output, int size) {
  int i, j, k, len;
  unsigned int block;
  char c;
  const char *ptr;
  __b64_error = B64_ERROR_NONE;

  /* Check input length */
  for(ptr = input; *ptr; ++ptr);
  len = (int)(ptr - input);
  if (len % 4) {
    __b64_error = B64_ERROR_INVALID_LEN;
    return;
  }

  /* Decode */
  for(i = j = 0; j < len; i += 3, j += 4) {
    block = 0;
    for(k = 0; k < 4; k++) {
      c = b64_reverse_table[input[j+k]];
      if (c == -1) {
        __b64_error = B64_ERROR_INVALID_CHAR;
        return;
      }
      block = (block << 6) | c;
    }
    output[i+0] = block >> 16;
    output[i+1] = (block >> 8) & 0xff;
    output[i+2] = block & 0xff;
  }

  /* Null terminate */
  output[i] = 0;
}

/**
 * b64chkerr: Check error
 */
int b64chkerr(void) {
  if (__b64_error) {
    return 1;
  } else {
    return 0;
  }
}

/**
 * b64errmsg: Convert error ID to error message
 */
const char *b64errmsg(void) {
  switch(__b64_error) {
  case B64_ERROR_NONE:
    return "Success";
  case B64_ERROR_INVALID_CHAR:
    return "Invalid Character";
  case B64_ERROR_INVALID_LEN:
    return "Padding Error";
  default:
    return "Unknown Error";
  }
}
