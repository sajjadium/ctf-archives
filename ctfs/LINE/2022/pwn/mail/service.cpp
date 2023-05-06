#include "service.h"
#include "mail_types.h"
#include "memory.h"
#include <iostream>
#include <unistd.h>
#include <string.h>

Service::Service(Memory *mem)
{
    memory = reinterpret_cast<struct mail *>(mem->getShMemory());
    memory->isServiceDone = false;
    bzero(owner, sizeof(owner));
}

Service::~Service()
{
    memory->error = true;
    turnOff();
}

void Service::SendCreateAccount()
{
    std::string buf;
    uint64_t size;

    std::cout << "= Input account id =" << std::endl;
    std::cin >> buf;
    if (std::cin.fail())
    {
        return;
    }

    size = buf.size();
    bzero(memory->accountId, sizeof(memory->accountId));
    memcpy(memory->accountId, buf.data(), (size > ACCOUNT_ID_MAXLEN) ? ACCOUNT_ID_MAXLEN : size);
    memory->accountIdSize = size;
    memory->cmd = CREATE_ACCOUNT;

    while ((memory->isCreateAccountSendedDone == false) && (memory->error == false))
        usleep(100);
    memory->isCreateAccountSendedDone = false;

    if (!memory->error)
    {
        std::cout << "Create " << buf.data() << std::endl;
    }
    else
    {
        handleError();
    }
}

void Service::SendLoginAccount()
{
    std::string buf;
    uint64_t size;

    std::cout << "= Input account id =" << std::endl;
    std::cin >> buf;
    if (std::cin.fail())
    {
        return;
    }

    size = buf.size();
    bzero(memory->accountId, sizeof(memory->accountId));
    memcpy(memory->accountId, buf.data(), (size > ACCOUNT_ID_MAXLEN) ? ACCOUNT_ID_MAXLEN : size);
    memory->accountIdSize = size;
    memory->cmd = LOGIN_ACCOUNT;

    while ((memory->isLoginAccountSendedDone == false) && (memory->error == false))
        usleep(100);
    memory->isLoginAccountSendedDone = false;

    if (!memory->error && isLogin())
    {
        memcpy(owner, buf.data(), buf.length());
        std::cout << "Hello, " << owner << std::endl;
    }
    else
    {
        handleError();
    }
}

int Service::SendMessage()
{
    std::string buf;
    uint64_t size;

    if (!isLogin())
        return 0;

    std::cout << "= Input your message =" << std::endl;
    std::cin >> buf;
    if (std::cin.fail())
    {
        return 0;
    }

    size = buf.size();
    bzero(memory->message, sizeof(memory->accountId));
    memcpy(memory->message, buf.data(), (size > MESSAGE_MAXLEN) ? MESSAGE_MAXLEN : size);
    memory->messageSize = size;

    std::cout << "= To whom =" << std::endl;
    std::cin >> buf;
    if (std::cin.fail())
    {
        return 0;
    }

    size = buf.size();
    bzero(memory->accountId, sizeof(memory->accountId));
    memcpy(memory->accountId, buf.data(), (size > ACCOUNT_ID_MAXLEN) ? ACCOUNT_ID_MAXLEN : size);
    memory->accountIdSize = size;

    memory->cmd = SEND_MESSAGE;

    while ((memory->isSendMessageSendedDone == false) && (memory->error == false))
        usleep(100);
    memory->isSendMessageSendedDone = false;

    if (!memory->error)
    {
        std::cout << "Sent message" << std::endl;
    }
    else
    {
        handleError();
    }

    return 0;
}

void Service::SendInbox()
{
    uint64_t index;
    if (!isLogin())
        return;

    std::cout << "= Input message index =" << std::endl;
    std::cin >> index;
    if (std::cin.fail())
    {
        return;
    }

    memcpy(memory->accountId, owner, ACCOUNT_ID_MAXLEN);
    memory->inboxIndex = index;
    memory->cmd = INBOX;

    while ((memory->isInboxSendedDone == false) && (memory->error == false))
        usleep(100);
    memory->isInboxSendedDone = false;

    if (!memory->error)
    {
        std::cout << "Inbox message" << std::endl;
        std::cout << memory->inboxMessage << std::endl;
    }
    else
    {
        handleError();
    }
}

void Service::SendDeleteMessage()
{
    uint64_t index;
    if (!isLogin())
        return;

    std::cout << "Input message index =" << std::endl;
    std::cin >> index;
    if (std::cin.fail())
    {
        return;
    }

    bzero(memory->accountId, sizeof(memory->accountId));
    memcpy(memory->accountId, owner, ACCOUNT_ID_MAXLEN);
    memory->inboxIndex = index;
    memory->cmd = DELETE_MESSAGE;

    while ((memory->isSendDeleteMessageSendedDone == false) && (memory->error == false))
        usleep(100);
    memory->isSendDeleteMessageSendedDone = false;

    if (!memory->error)
    {
        std::cout << "Deleted" << std::endl;
    }
    else
    {
        handleError();
    }
}

void Service::Logout()
{
    memory->isLogin = false;
    bzero(owner, sizeof(owner));
}

void Service::turnOff()
{
    memory->isServiceDone = true;
}

void Service::handleError()
{
    std::cout << "Error..." << std::endl;
    memory->error = false;
}

bool Service::ServiceDone()
{
    return memory->isServiceDone;
}

bool Service::isLogin()
{
    return memory->isLogin;
}