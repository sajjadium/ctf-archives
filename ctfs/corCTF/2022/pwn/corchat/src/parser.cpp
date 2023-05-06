#include "parser.h"

bool Parser::IsValid(char *buf, size_t buf_len)
{
    for (int i = 0; i < sizeof(COR_MSG_TYPES) / sizeof(COR_MSG_TYPES[0]); i++)
    {
        if (strcmp(COR_MSG_TYPES[i], buf) == 0)
            return true;
    }
    return false;
};
