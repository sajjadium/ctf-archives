#include <stdint.h>
#include <vector>
#include <string>
#define ACCOUNT_ID_MAXLEN 32
#define MESSAGE_MAXLEN 0x400

enum command_type
{
    CREATE_ACCOUNT,
    LOGIN_ACCOUNT,
    SEND_MESSAGE,
    INBOX,
    DELETE_MESSAGE,
    LOGOUT_ACCOUNT,
    TURN_OFF,
    CLEAR
};

struct mail
{
    uint64_t userId;
    unsigned char cmd;
    bool isLogin;
    bool isCreateAccountSendedDone;
    bool isLoginAccountSendedDone;
    bool isSendMessageSendedDone;
    bool isSendDeleteMessageSendedDone;
    bool isInboxSendedDone;
    bool isServiceDone;
    bool error;
    char accountId[ACCOUNT_ID_MAXLEN + 1];
    uint64_t accountIdSize;
    char message[MESSAGE_MAXLEN + 1];
    uint64_t messageSize;
    char inboxMessage[MESSAGE_MAXLEN + 1];
    uint64_t inboxIndex;
};

struct mail_message
{
    mail_message() : message(NULL), messageSize(0), to(NULL) {}
    virtual ~mail_message()
    {
        delete message;
        delete to;

        message = NULL;
        messageSize = 0;
        to = NULL;
    }

    char *getMessage() { return message; }
    uint64_t getMessageSize() { return messageSize; }
    char *getTo() { return to; }

    void setMessage(char *message_)
    {
        message = message_;
    }
    void setMessageSize(uint64_t size)
    {
        messageSize = size;
    }
    void setTo(char *to_)
    {
        to = to_;
    }

    char *message;
    uint64_t messageSize;
    char *to;
};