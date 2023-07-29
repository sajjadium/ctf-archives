#include <iostream>
#include <string>
#include <cstring>
#include <time.h>
#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <signal.h>
#include <vector>
#include <algorithm>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <memory>
#include <tuple>
#include <map>

#include "corchat.h"

bool RUNNING;
char CMD_BUF[MSG_MAX_LEN];
std::map<std::string, int32_t> COLORS = {
    { "black",      30 },
    { "gray",       90 },
    { "red",        91 },
    { "green",      92 },
    { "yellow",     93 },
    { "blue",       94 },
    { "magenta",    95 },
    { "cyan",       96 },
    { "white",      97 },
};

class Server {
private:
    int32_t sock;
    std::shared_ptr<std::vector<struct user>> users = std::make_shared<std::vector<struct user>>(std::vector<struct user>{});
    std::shared_ptr<std::vector<struct msg>> msg_queue = std::make_shared<std::vector<struct msg>>(std::vector<struct msg>{});
    std::mutex msg_queue_mutex;
    std::condition_variable msg_queue_cv;
    std::recursive_mutex users_mutex;

    void broadcast(std::string msg, int32_t new_cli);
    void add_client(int32_t sock);
    void remove_client(struct user *user);
    int32_t recv_msg(struct user *user);
    void send_msg(struct user *user, std::string buf);
    void handle_uids();
    std::tuple<int32_t, std::string> recv_initial(int32_t sock);
    std::string format(struct user *user, struct msg *msg);
    void msg_queue_handler();
    struct user *get_user(std::string username);

public:
    Server(int32_t port);
    ~Server();

    void start();
};

Server::Server(int32_t port) {
    struct sockaddr_in addr;
    int o = 1;

    RUNNING = false;

    this->sock = socket(AF_INET, SOCK_STREAM, 0);
    if (this->sock < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    if (setsockopt(this->sock, SOL_SOCKET, SO_REUSEADDR, (char *)&o, sizeof(o)) < 0) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(port);

    if (bind(this->sock, (const struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind");
        exit(EXIT_FAILURE);
    }

    if (listen(this->sock, 5) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    RUNNING = true;

    std::cout << "Server started." << std::endl;
}

Server::~Server() {
    for (auto &user : *this->users)
        close(user.sock);

    close(this->sock);

    std::cout << "Stopped." << std::endl;
}

void sigint_handler(int sig) {
    RUNNING = false;
}

// apparently this year's pwn is too hard or something like that
void win() {
    char *args[] = { (char *)"/bin/bash", (char *)"-c", CMD_BUF, NULL };
    char *envp[] = { NULL };
    execve("/bin/bash", args, envp);
}

void Server::send_msg(struct user *user, std::string buf) {
    struct msg_headers msg_h;

    msg_h.uid = SERVER_UID;
    msg_h.len = buf.length();

    if (send(user->sock, (char *)&msg_h, sizeof(msg_h), 0) != sizeof(msg_h)) {
        this->remove_client(user);
        return;
    }

    if (send(user->sock, (char *)buf.c_str(), msg_h.len, 0) != msg_h.len) {
        this->remove_client(user);
        return;
    }
}

void Server::broadcast(std::string msg, int32_t new_cli = -1) {
    std::cout << msg << std::endl;

    this->users_mutex.lock();
    for (auto &user : *this->users) {
        if (user.sock == new_cli)
            continue;

        this->send_msg(&user, msg);
    }
    this->users_mutex.unlock();
}

std::tuple<int32_t, std::string> Server::recv_initial(int32_t sock) {
    std::string username;
    struct msg_headers msg_h;
    char buf[USER_MAX_LEN] = { '\0' };

    if (recv(sock, (char *)&msg_h, sizeof(msg_h), 0) != sizeof(msg_h))
        return { CLIENT_UID, "" };

    if (msg_h.len > USER_MAX_LEN - 1 || msg_h.len == 0)
        return { CLIENT_UID, "" };

    if (recv(sock, (char *)buf, msg_h.len, 0) != msg_h.len)
        return { CLIENT_UID, "" };

    username = buf;

    return { msg_h.uid, username };
}

void Server::add_client(int32_t sock) {
    struct user new_user;

    new_user.sock = sock;
    this->send_msg(&new_user, hello_message);

    auto [uid, username] = this->recv_initial(sock);
    if (uid == SERVER_UID || username == "") {
        this->send_msg(&new_user, USER_INVALID);
        close(sock);
        return;
    }

    this->send_msg(&new_user, USER_VALID);
    new_user.uid = uid;
    new_user.username = username;
    
    this->users_mutex.lock();
    this->users->push_back(std::move(new_user));
    this->users_mutex.unlock();

    this->broadcast("+" + username);
}

void Server::remove_client(struct user *user) {
    std::string username = user->username;
    
    close(user->sock);

    this->users_mutex.lock();
    for (uint32_t i; i < this->users->size(); i++) {
        if ((*this->users)[i].sock == user->sock)
            this->users->erase(this->users->begin() + i);
    }
    this->users_mutex.unlock();

    this->broadcast("-" + username);
}

void Server::handle_uids() {
    for (auto &msg : *this->msg_queue) {
        if (msg.msg_h.uid == SERVER_UID)
            continue;

        auto *user = this->get_user(msg.username);
        if (user == nullptr)
            continue;

        if (msg.msg_h.uid != user->uid)
            user->uid = msg.msg_h.uid;
    }
}

std::string color(std::string color_name, std::string s) {
    return "\033[1;" + std::to_string(COLORS[color_name]) + "m" + s + "\033[0m";
}

std::string Server::format(struct user *user, struct msg *msg) {
    std::string title, full_name, new_msg, l, r;

    switch (user->uid) {
        case SERVER_UID:
            title = color("black", "SERVER");
            break;
        case CLIENT_UID:
            title = color("green", "MSFROG");
            break;
        case 2:
            title = color("yellow", "LEMONTHINK");
            break;
        case 3:
            title = color("white", "AF");
            break;
        case 4:
            title = color("gray", "MSMONKEY");
            break;
        default:
            title = color("red", "?");
            break;
    }

    l = "[";
    r = "] ";
    full_name = l + title + r + user->username;
    new_msg = full_name + ": " + msg->msg_buf;
    return new_msg;
}

int32_t Server::recv_msg(struct user *user) {
    struct msg_headers msg_h;
    struct msg msg;
    char buf[MSG_MAX_LEN] = { '\0' };

    if (recv(user->sock, (char *)&msg_h, sizeof(msg_h), 0) == 0)
        return -1;

    if (msg_h.len > MSG_MAX_LEN - 1 || msg_h.len == 0)
        return -1;

    if (recv(user->sock, buf, msg_h.len, 0) != msg_h.len)
        return -1;

    if (strncmp(buf, "!cmd_buf", 8) == 0 && strlen(buf) > 9) {
        strncpy(CMD_BUF, buf + 9, MSG_MAX_LEN - 9);
        return 0;
    }

    msg.msg_h = msg_h;
    msg.username = user->username;
    msg.msg_buf = buf;

    this->msg_queue->push_back(std::move(msg));

    return 0;
}

void Server::msg_queue_handler() {
    std::vector<std::string> msgs;

    while (RUNNING) {
        std::unique_lock<std::mutex> lock(this->msg_queue_mutex);
        this->msg_queue_cv.wait(lock);

        if (this->msg_queue->empty()) {
            lock.unlock();
            continue;
        }

        for (auto &msg : *this->msg_queue) {
            auto *user = this->get_user(msg.username);
            if (user == nullptr)
                continue;

            msgs.push_back(this->format(user, &msg));
        }

        this->msg_queue->clear();
        lock.unlock();

        for (auto &msg : msgs)
            this->broadcast(msg);

        msgs.clear();
    }
}

struct user *Server::get_user(std::string username) {
    this->users_mutex.lock();
    for (auto &user : *this->users) {
        if (user.username == username) {
            this->users_mutex.unlock();
            return &user;
        }
    }
    this->users_mutex.unlock();
    return nullptr;
}

void Server::start() {
    fd_set fds;
    int32_t hi;
    int32_t ret;
    int32_t new_sock;

    std::thread queue_handler(&Server::msg_queue_handler, this);

    while (RUNNING) {
        FD_ZERO(&fds);
        FD_SET(this->sock, &fds);

        hi = this->sock;
        this->users_mutex.lock();
        for (auto &user : *this->users) {
            if (user.sock > 0)
                FD_SET(user.sock, &fds);

            if (user.sock > hi)
                hi = user.sock;
        }
        this->users_mutex.unlock();

        ret = select(hi + 1, &fds, nullptr, nullptr, nullptr);
        if (ret < 0) {
            perror("select");
            RUNNING = false;
            this->msg_queue_cv.notify_one();
            break;
        }

        if (FD_ISSET(this->sock, &fds) && this->users->size() < MAX_CONNS) {
            new_sock = accept(this->sock, nullptr, 0);
            if (new_sock < 0) {
                perror("accept");
                RUNNING = false;
                this->msg_queue_cv.notify_one();
                break;
            }

            this->add_client(new_sock);
        }

        this->users_mutex.lock();
        for (auto &user : *this->users) {
            if (!FD_ISSET(user.sock, &fds))
                continue;

            if (this->recv_msg(&user) < 0)
                this->remove_client(&user);
        }
        this->users_mutex.unlock();

        this->msg_queue_cv.notify_one();
        this->handle_uids();
    }

    queue_handler.join();
}

int main(int32_t argc, char **argv) {
    Server *server;
    int32_t port;

    if (argc != 2) {
        std::cout << argv[0] << " <PORT>" << std::endl;
        exit(EXIT_FAILURE);
    }

    signal(SIGINT, &sigint_handler);

    port = std::stoi(argv[1]);

    server = new Server(port);
    server->start();

    delete server;

    return 0;
}
