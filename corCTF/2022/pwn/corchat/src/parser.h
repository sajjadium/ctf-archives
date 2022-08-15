#ifndef COR_PARSER_H
#define COR_PARSER_H

#include <unistd.h>
#include <cstring>
#include "message.h"

class Parser
{
    public:
        static bool IsValid(char *buf, size_t buf_len);
        static bool IsUnameLenValid(size_t len);
};

#endif
