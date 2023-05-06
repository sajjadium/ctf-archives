#ifndef __HEADER_BASE64__
#define __HEADER_BASE64__

#define B64_ERROR_NONE         0
#define B64_ERROR_INVALID_CHAR 1
#define B64_ERROR_INVALID_LEN  2

extern int __b64_error;

void b64decode(const char *input, char *output, int size);
void b64encode(const char *input, char *output, int size);
int b64chkerr(void);
const char *b64errmsg(void);

#endif
