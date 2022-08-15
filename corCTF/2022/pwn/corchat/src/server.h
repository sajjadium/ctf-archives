#ifndef COR_SERVER_H
#define COR_SERVER_H

#include <iostream>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdint.h>
#include "cstring"
#include <sstream>

#include "crusader.h"

#define MAX_CRUSADERS 4

class ChatServer
{
    public:
        ChatServer(int port);
        ~ChatServer();
        int StartListening();
        void MainLoop();
        void BroadcastMsg(Crusader *sender, const char *msg, size_t msg_size, bool add_delim);

    private:
        int m_port;
        int8_t m_sock_fd;
        int8_t m_connected_crusaders;
        fd_set m_master_fds;
        sockaddr_in m_sock_addr;
        Crusader *m_crusader_seats[MAX_CRUSADERS] = {nullptr};
        static const std::string m_welcome_msg;

        int8_t AcceptCrusader(int8_t client_fd);
        static void *RecvCrusaderMessages(void *context);
};

#endif
