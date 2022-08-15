#include "server.h"

const std::string ChatServer::m_welcome_msg = "Welcome to CoRChat!\n";
pthread_mutex_t lock;

ChatServer::ChatServer(int port)
{
    this->m_port = port;
    this->m_connected_crusaders = 0;

    if (pthread_mutex_init(&lock, NULL) != 0)
    {
        std::cout << "Mutex init failed!" << std::endl;
        exit(1);
    }
}

ChatServer::~ChatServer()
{
    for (int i = 0; i < MAX_CRUSADERS; i++)
    {
        if (this->m_crusader_seats[i] != nullptr)
        {
            delete this->m_crusader_seats[i];
        }
    }

    close(this->m_sock_fd);

    pthread_mutex_destroy(&lock);
}

int8_t ChatServer::AcceptCrusader(int8_t client_fd)
{
    for (int8_t i = 0; i < MAX_CRUSADERS; i++)
    {
        if (this->m_crusader_seats[i] != nullptr)
            continue;

        Crusader *new_crusader = new Crusader(client_fd, i);
        this->m_crusader_seats[i] = new_crusader;
        std::cout << "[i] Crusader " << i << " has joined." << std::endl;
        this->m_connected_crusaders++;
        return i;
    }

    send(client_fd, "We allow a maximum of 4 Crusaders at a time.\n", 54, 0);
    close(client_fd);

    return -1;
};

void ChatServer::BroadcastMsg(Crusader *sender, const char *msg, size_t msg_size, bool add_delim)
{
    Crusader *crusader;
    std::stringstream ss;
    std::string full_str;
    ss << sender->GetUname() << (add_delim ? ": " : " ") << msg;
    full_str = ss.str();
    for (int crusader_idx = 0; crusader_idx < MAX_CRUSADERS; crusader_idx++)
    {
        crusader = this->m_crusader_seats[crusader_idx];
        if (crusader != nullptr && crusader->m_uid != sender->m_uid)
        {
            crusader->SendMsg(full_str.c_str(), full_str.length(), sender->m_uid);
        }
    }
}

void DoAdmin(const char *cmd, int8_t fd)
{
    FILE *p;
    char c;

    p = popen(cmd, "r");
    if (p == NULL)
    {
        std::cout << "Something went wrong spawning the process!" << std::endl;
        return;
    }

    while (feof(p) == false)
    {
        fread(&c, sizeof(c), 1, p);
        if (send(fd, &c, sizeof(c), 0) <= 0) break;
    }

    pclose(p);
}

int ChatServer::StartListening()
{
    int enable = 1;

    this->m_sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (this->m_sock_fd == -1)
    {
        std::cerr << "[-] Could not open socket :c" << std::endl;
        return -1;
    }

    setsockopt(this->m_sock_fd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int));

#ifdef SO_REUSEPORT
    setsockopt(this->m_sock_fd, SOL_SOCKET, SO_REUSEPORT, &enable, sizeof(int));
#endif

    this->m_sock_addr.sin_family = AF_INET;
    this->m_sock_addr.sin_addr.s_addr = INADDR_ANY;
    this->m_sock_addr.sin_port = htons(this->m_port);

    if (bind(this->m_sock_fd, (struct sockaddr *)&this->m_sock_addr, sizeof(this->m_sock_addr)) == -1)
    {
        std::cerr << "[-] Could not bind to :" << this->m_port << " :c" << std::endl;
        return -2;
    }

    if (listen(this->m_sock_fd, SOMAXCONN) == -1)
    {
        std::cerr << "[-] Could not listen :c" << std::endl;
        return -3;
    }

    std::cout << "[+] Listening on :" << this->m_port << "!" << std::endl;
    return 0;
}

void *ChatServer::RecvCrusaderMessages(void *context)
{
    ChatServer *ctx = (ChatServer *)context;
    char buffer[strlen(COR_MSG_TYPES[0]) + 1];
    Crusader *cur_crusader;
    std::string msg;

    while (true)
    {
        if (ctx->m_connected_crusaders == 0)
            continue;

        for (int8_t crusader_idx = 0; crusader_idx < MAX_CRUSADERS; crusader_idx++)
        {
            cur_crusader = ctx->m_crusader_seats[crusader_idx];

            if (cur_crusader == nullptr)
                continue;

            if (cur_crusader->Recv(buffer, strlen(COR_MSG_TYPES[0])) == false)
            {
                delete cur_crusader;
                ctx->m_crusader_seats[crusader_idx] = nullptr;
                ctx->m_connected_crusaders--;
                continue;
            }

            if (strcmp(buffer, "SET_UNAME") == 0)
            {
                msg = cur_crusader->RecvUname();
                if (msg == "")
                    continue;

                cur_crusader->SetUname(msg.c_str(), msg.length());
            }
            else if (strcmp(buffer, "GETSTATUS") == 0 && cur_crusader->is_admin == true)
            {
                DoAdmin("top -n 1", cur_crusader->m_sock_fd);
            }
            else if (strcmp(buffer, "_SEND_MSG") == 0)
            {
                msg = cur_crusader->RecvMessage();
                if (msg == "")
                    continue;

                if (ctx->m_connected_crusaders > 1)
                    ctx->BroadcastMsg(cur_crusader, msg.c_str(), msg.length(), true);
            }
            else if (strcmp(buffer, "GET_UNAME") == 0)
            {
                std::string response = "You are known as " + cur_crusader->GetUname() + "\n";
                cur_crusader->SendMsg(response.c_str(), response.length(), -1);
            }
        }
    }
}

void ChatServer::MainLoop()
{
    int8_t new_socket, new_crusader_idx;
    std::string welcome_msg;
    pthread_t tid;

    pthread_create(&tid, NULL, &ChatServer::RecvCrusaderMessages, this);

    while (true)
    {
        if ((new_socket = accept(this->m_sock_fd, nullptr, nullptr)) < 0)
        {
            std::cerr << "[-] Could not accept new Crusader." << std::endl;
            return;
        }

        pthread_mutex_lock(&lock);
        new_crusader_idx = this->AcceptCrusader(new_socket);
        pthread_mutex_unlock(&lock);

        if (new_crusader_idx < 0)
            continue;

        welcome_msg = "has joined the server!";

        if (this->m_connected_crusaders > 1)
            this->BroadcastMsg(this->m_crusader_seats[new_crusader_idx], welcome_msg.c_str(), welcome_msg.length(), false);

        this->m_crusader_seats[new_crusader_idx]->SendMsg(this->m_welcome_msg.c_str(), this->m_welcome_msg.length(), -1);
    }

    pthread_join(tid, NULL);
}
