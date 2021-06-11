#ifndef __OGET_H__
#define __OGET_H__

#define SIZE_HEADER   0x20  /* 'GET /? HTTP/1.1\r\nHost: ?:XXXXX\r\n\r\n' */
#define SIZE_HOST     0x0d  /* http://?:XXXXX */
#define SIZE_RESPONSE 0x200

void fatal(char*);
char* omega_get(char*);

#endif
