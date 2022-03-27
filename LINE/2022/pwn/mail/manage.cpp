#include "manage.h"
#include "memory.h"
#include "mail_types.h"
#include <iostream>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <algorithm>

Manage::Manage(Memory *mem)
{
    memory = reinterpret_cast<struct mail *>(mem->getShMemory());
    memory->isCreateAccountSendedDone = false;
    memory->isLoginAccountSendedDone = false;
    memory->isSendMessageSendedDone = false;
    memory->isSendDeleteMessageSendedDone = false;
    memory->isInboxSendedDone = false;
    memory->isLogin = false;
    memory->error = false;
    memory->isServiceDone = false;

    ResetCommand();
}

Manage::~Manage()
{
    memory->isServiceDone = true;
    error();
    for (uint64_t i = 0; i < accountIds.size(); i++)
    {
        delete accountIds.at(i);
    }
    accountIds.clear();

    for (uint64_t i = 0; i < messages.size(); i++)
    {
        delete messages.at(i);
    }
    messages.clear();
}

void Manage::ResetCommand()
{
    memory->cmd = CLEAR;
}

void Manage::ReceiveCreateAccount()
{
    char *accountId = NULL;
    uint64_t size = 0;

    if (getCmd() == CREATE_ACCOUNT)
    {
        if (memory->accountIdSize > ACCOUNT_ID_MAXLEN)
        {
            error();
            return;
        }

        usleep(100);
        accountId = new char[ACCOUNT_ID_MAXLEN + 1];
        if (!accountId)
        {
            error();
            return;
        }

        bzero(accountId, ACCOUNT_ID_MAXLEN + 1);
        memcpy(accountId, memory->accountId, memory->accountIdSize);
        size = countAccount(accountId);
        if (size > 0)
        {
            error();
            return;
        }
        accountIds.push_back(accountId);

        size = countAccount(accountId);
        ResetCommand();
        memory->isCreateAccountSendedDone = true;
    }
}

void Manage::ReceiveLoginAccount()
{
    if (getCmd() == LOGIN_ACCOUNT)
    {
        for (uint64_t i = 0; i < accountIds.size(); i++)
        {
            if (memory->accountIdSize > ACCOUNT_ID_MAXLEN)
            {
                error();
                return;
            }

            if (!strcmp(accountIds.at(i), memory->accountId))
            {
                usleep(100);
                ResetCommand();
                memory->isLogin = true;
                break;
            }
        }
        memory->isLoginAccountSendedDone = true;
    }
}

uint64_t Manage::countAccount(char *id)
{
    char *accountId = NULL;
    uint64_t count = 0;
    for (uint64_t i = 0; i < accountIds.size(); i++)
    {
        accountId = accountIds.at(i);
        if (!strcmp(id, accountId))
        {
            count++;
        }
    }
    return count;
}

void Manage::ReceiveSendMessage()
{
    struct mail_message *mmsg = NULL;
    char *message = NULL, *to = NULL;
    uint64_t size = 0;

    if (getCmd() == SEND_MESSAGE)
    {
        if (memory->accountIdSize > ACCOUNT_ID_MAXLEN)
        {
            error();
            return;
        }
        to = new char[ACCOUNT_ID_MAXLEN + 1];
        if (!to)
        {
            error();
            return;
        }

        bzero(to, ACCOUNT_ID_MAXLEN + 1);
        memcpy(to, memory->accountId, memory->accountIdSize);

        size = countAccount(to);
        if (!size)
        {
            error();
            return;
        }

        memory->isSendMessageSendedDone = true;

        if (memory->messageSize > MESSAGE_MAXLEN)
        {
            error();
            return;
        }

        usleep(100);
        message = new char[MESSAGE_MAXLEN + 1];
        if (!message)
        {
            error();
            return;
        }

        mmsg = new struct mail_message;
        if (!mmsg)
        {
            error();
            return;
        }

        mmsg->setMessage(message);
        mmsg->setMessageSize(memory->messageSize);
        mmsg->setTo(to);

        bzero(message, MESSAGE_MAXLEN + 1);
        memcpy(message, memory->message, memory->messageSize);

        messages.push_back(mmsg);
        ResetCommand();
    }
}

uint64_t Manage::countInbox(char *owner)
{
    struct mail_message *mmsg = NULL;
    uint64_t count = 0;
    for (uint64_t i = 0; i < messages.size(); i++)
    {
        mmsg = messages.at(i);
        if (!strcmp(owner, mmsg->getTo()))
        {
            count++;
        }
    }
    return count;
}

struct mail_message *Manage::getInbox(char *owner, uint64_t index)
{
    struct mail_message *mmsg = NULL;
    uint64_t count = 0;
    for (uint64_t i = 0; i < messages.size(); i++)
    {
        mmsg = messages.at(i);
        if (!strcmp(owner, mmsg->getTo()))
        {
            if (count == index)
            {
                return mmsg;
            }
            count++;
        }
    }
    return NULL;
}

void Manage::ReceiveInbox()
{
    struct mail_message *mmsg = NULL;
    char *owner = NULL;
    uint64_t size = 0;

    if (getCmd() == INBOX)
    {
        owner = memory->accountId;
        size = countInbox(owner);

        if (memory->inboxIndex >= size)
        {
            error();
            return;
        }

        usleep(100);
        mmsg = getInbox(owner, memory->inboxIndex);
        if (!mmsg)
        {
            error();
            return;
        }

        bzero(memory->inboxMessage, sizeof(memory->inboxMessage));
        memcpy(memory->inboxMessage, mmsg->getMessage(), mmsg->getMessageSize());

        ResetCommand();
        memory->isInboxSendedDone = true;
    }
}

void Manage::ReceiveSendDeleteMessage()
{
    char tmp[0x30] = {
        0,
    };
    struct mail_message *mmsg = NULL;
    struct mail_message *target = NULL;
    char *owner = NULL;
    uint64_t size = 0;

    if (getCmd() == DELETE_MESSAGE)
    {
        owner = memory->accountId;
        size = countInbox(owner);

        if (memory->inboxIndex >= size)
        {
            error();
            return;
        }

        usleep(100);
        mmsg = getInbox(owner, memory->inboxIndex);
        if (!mmsg)
        {
            error();
            return;
        }

        for (uint64_t i = 0; i < messages.size(); i++)
        {
            target = messages.at(i);
            if (target == mmsg)
            {
                messages.erase(messages.begin() + i);
                delete target;
            }
        }

        ResetCommand();
        memory->isSendDeleteMessageSendedDone = true;
    }
}

unsigned char Manage::getCmd()
{
    return memory->cmd;
}

bool Manage::ServiceDone()
{
    return memory->isServiceDone;
}

void Manage::error()
{
    memory->error = true;
    ResetCommand();
}