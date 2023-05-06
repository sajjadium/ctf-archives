#include <signal.h>
#include <unistd.h>
#include <iostream>
#include <cstdlib>
#include <string.h>
#include <fcntl.h>

#include "manage.h"
#include "memory.h"
#include "service.h"
#include "mail_types.h"

void alarm_handler(int signo)
{
    exit(0);
}

void service_menu(Service *srv)
{
    int menu_num = 0;

    alarm(30);
    signal(SIGALRM, alarm_handler);

    std::cout << "Spawn new service\n"
              << std::endl;
    while (!srv->ServiceDone())
    {
        std::cout << "==================" << std::endl;
        std::cout << "0. create account" << std::endl;
        std::cout << "1. login account" << std::endl;
        std::cout << "2. send message" << std::endl;
        std::cout << "3. inbox" << std::endl;
        std::cout << "4. delete message" << std::endl;
        std::cout << "5. logout account" << std::endl;
        std::cout << "6. turn off" << std::endl;
        std::cout << "==================" << std::endl;

        std::cin >> menu_num;
        if (std::cin.fail())
        {
            return;
        }

        switch (menu_num)
        {
        case CREATE_ACCOUNT:
            srv->SendCreateAccount();
            break;

        case LOGIN_ACCOUNT:
            srv->SendLoginAccount();
            break;

        case SEND_MESSAGE:
            srv->SendMessage();
            break;

        case INBOX:
            srv->SendInbox();
            break;

        case DELETE_MESSAGE:
            srv->SendDeleteMessage();
            break;

        case LOGOUT_ACCOUNT:
            srv->Logout();
            break;

        case TURN_OFF:
            srv->turnOff();
            break;

        default:
            return;
        }
    }
}

void manage_menu(Manage *mgr)
{
    alarm(30);
    signal(SIGALRM, alarm_handler);

    while (!mgr->ServiceDone())
    {
        switch (mgr->getCmd())
        {
        case CREATE_ACCOUNT:
            mgr->ReceiveCreateAccount();
            break;

        case LOGIN_ACCOUNT:
            mgr->ReceiveLoginAccount();
            break;

        case SEND_MESSAGE:
            mgr->ReceiveSendMessage();
            break;

        case INBOX:
            mgr->ReceiveInbox();
            break;

        case DELETE_MESSAGE:
            mgr->ReceiveSendDeleteMessage();
            break;

        default:
            break;
        }
        usleep(100);
    }
}

int main()
{
    uint32_t key = 0;
    int fd;

    fd = open("/dev/urandom", 0);
    read(fd, &key, sizeof(key));
    close(fd);

    Memory *mem = new Memory(key);
    mem->createShMemory();

    if (fork() == 0)
    {
        Manage *mgr = new Manage(mem);
        manage_menu(mgr);
        delete mgr;
        delete mem;
    }
    else
    {
        Service *srv = new Service(mem);
        service_menu(srv);
        delete srv;
    }

    return 0;
}