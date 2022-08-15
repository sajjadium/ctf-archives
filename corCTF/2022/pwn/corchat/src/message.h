#ifndef COR_MESSAGE_H
#define COR_MESSAGE_H

#include <stdint.h>

#define MAX_MSG_SIZE 4096

[[maybe_unused]] static char COR_MSG_TYPES[4][10] = {
    "SET_UNAME",
    "GET_UNAME",
    "_SEND_MSG",
    "GETSTATUS"
};

typedef struct {
    char buffer[1024];
    uint16_t flags;
    uint16_t len;
} cor_msg_buf;

typedef struct {
    char buffer[32];
    uint16_t len;
} cor_uname_buf;

#endif
