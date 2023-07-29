#include <iostream>
#include <string>
#include <thread>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <signal.h>

#include "corchat.h"

bool running;
int32_t CURR_uid = CLIENT_UID;

class Client {
private:
    int32_t sock;

public:
    Client(std::string ip, int32_t port);
    ~Client();

    void interactive();
    int32_t send_msg(std::string s);
    std::string recv_msg();
    void recv_msgs();
};

Client::Client(std::string ip, int32_t port) {
    struct sockaddr_in addr;
    struct timeval timeout;
    std::string hello;
    std::string username;

    running = false;

    std::cout << "Enter username: ";
    std::getline(std::cin, username);

    if (username.length() == 0 || username.length() > USER_MAX_LEN) {
        std::cout << "Invalid username." << std::endl;
        exit(EXIT_FAILURE);
    }

    std::cout << "Connecting to " << ip << ":" << port << " as " << username << "... " << std::flush;

    this->sock = socket(AF_INET, SOCK_STREAM, 0);
    if (this->sock < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    timeout.tv_sec = CLI_TIMEOUT;
    timeout.tv_usec = 0;

    if (setsockopt(this->sock, SOL_SOCKET, SO_RCVTIMEO, (char *)&timeout, sizeof(timeout)) < 0) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);

    if (inet_pton(AF_INET, ip.c_str(), &addr.sin_addr) <= 0) {
        perror("inet_pton");
        exit(EXIT_FAILURE);
    }

    if (connect(this->sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("connect");
        exit(EXIT_FAILURE);
    }

    std::cout << "connected." << std::endl;

    hello = this->recv_msg();
    if (hello == "") {
        std::cout << "Something went wrong receiving the hello message." << std::endl;
        return;
    }

    std::cout << hello << std::endl;

    if (this->send_msg(username) < 0) {
        std::cout << "Something went wrong sending username." << std::endl;
        return;
    }

    if (this->recv_msg() == USER_INVALID) {
        std::cout << "Username \"" << username << "\" is invalid." << std::endl;
        return;
    }

    running = true;
}

Client::~Client() {
    close(this->sock);

    std::cout << "Disconnected." << std::endl;
}

std::string Client::recv_msg() {
    struct msg_headers msg_h;
    char buf[MSG_MAX_LEN] = { '\0' };
    std::string msg;

    if (recv(this->sock, (char *)&msg_h, sizeof(msg_h), 0) != sizeof(msg_h))
        return "";

    if (msg_h.len > sizeof(buf) - 1)
        return "";

    if (recv(this->sock, (char *)buf, msg_h.len, 0) != msg_h.len)
        return "";

    msg = buf;

    return msg;
}

void Client::recv_msgs() {
    std::string msg;

    while (running) {
        msg = this->recv_msg();
        if (msg != "")
            std::cout << msg << std::endl;
    }
}

int32_t Client::send_msg(std::string s) {
    struct msg_headers msg_h;

    if (s.length() > MSG_MAX_LEN - 1)
        return -1;

    msg_h.uid = CURR_uid;
    msg_h.len = s.length();

    if (send(this->sock, (char *)&msg_h, sizeof(msg_h), 0) != sizeof(msg_h)) {
        running = false;
        return -1;
    }

    if (send(this->sock, (char *)s.c_str(), s.length(), 0) != s.length()) {
        running = false;
        return -1;
    }

    return 0;
}

void Client::interactive() {
    std::string msg;

    std::thread recv_thread(&Client::recv_msgs, this);

    while (running) {
        std::getline(std::cin, msg);

        if (msg == "!exit" || msg == "!quit") {
            running = false;
            break;
        }

        if (msg.substr(0, 4) == "!uid") {
            auto new_uid = msg.substr(msg.find(" ") + 1);
            if (new_uid != "!uid" && new_uid.length() != 0) {
                auto uid_num = std::stoi(new_uid);

                if (uid_num == SERVER_UID)
                    continue;

                if (uid_num > 4)
                    uid_num = 5;

                CURR_uid = uid_num;
            }

            continue;
        }

        if (msg.length() == 0)
            continue;

        if (this->send_msg(msg) < 0) {
            running = false;
            break;
        }
    }

    std::cout << "Waiting for recv_thread... " << std::flush;
    recv_thread.join();
    std::cout << "done." << std::endl;
}

int main(int32_t argc, char **argv) {;
    Client *cli;
    std::string ip;
    int32_t port;

    if (argc != 3) {
        std::cout << argv[0] << " <IP> <PORT>" << std::endl;
        exit(EXIT_FAILURE);
    }

    ip = argv[1];
    port = std::stoi(argv[2]);

    cli = new Client(ip, port);
    cli->interactive();

    delete cli;

    return 0;
}
