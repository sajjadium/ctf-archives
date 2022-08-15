#ifndef COR_CURSADER_H
#define COR_CRUSADER_H

#include <iostream>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sstream>
#include <cstring>

#include "parser.h"

class Crusader
{
    public:
        Crusader(int8_t client_fd, int uid);
        ~Crusader();
        int SendMsg(const char *msg, size_t msg_len, int8_t sender_id);
        bool Recv(char *buf, size_t buf_size);
        void UpdateUname(const char **uname, size_t len);
        void SetUname(const char *buf, size_t buf_size);
        std::string RecvMessage();
        std::string GetUname();
        std::string RecvUname();
        bool is_admin;
        int m_uid;
        int m_sock_fd;

    private:
        char *uname;
        size_t uname_len;
};

#endif
