#ifndef CORCHAT_H
#define CORCHAT_H

#define MSG_MAX_LEN     1024
#define USER_MAX_LEN    32

#define CLIENT_UID      1
#define SERVER_UID      0

#define MAX_CONNS       200

#define CLI_TIMEOUT     3

#define USER_VALID      "USER_VALID"
#define USER_INVALID    "USER_INVALID"

std::string hello_message = R"(
 ██████╗ ██████╗ ██████╗         
██╔════╝██╔═══██╗██╔══██╗        
██║     ██║   ██║██████╔╝        
██║     ██║   ██║██╔══██╗        
╚██████╗╚██████╔╝██║  ██║        
 ╚═════╝ ╚═════╝ ╚═╝  ╚═╝        
                                 
 ██████╗██╗  ██╗ █████╗ ████████╗
██╔════╝██║  ██║██╔══██╗╚══██╔══╝
██║     ███████║███████║   ██║   
██║     ██╔══██║██╔══██║   ██║   
╚██████╗██║  ██║██║  ██║   ██║   
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
)";

struct user {
    int32_t sock;
    int32_t uid;
    std::string username;
};

struct msg_headers {
    int32_t uid;
    size_t len;
};

struct msg {
    struct msg_headers msg_h;
    std::string username;
    std::string msg_buf;
};

#endif
