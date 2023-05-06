#include <vector>
#include <string>
#include <stdint.h>

class Memory;
struct mail;

class Manage
{
public:
    Manage(Memory *mem);
    ~Manage();
    void ReceiveCreateAccount();
    void ReceiveLoginAccount();
    void ReceiveSendMessage();
    void ReceiveSendDeleteMessage();
    void ResetCommand();
    bool ServiceDone();
    bool messageFiltering(char *message);
    void ReceiveInbox();
    void error();
    unsigned char getCmd();
    uint64_t countAccount(char *id);
    uint64_t countInbox(char *owner);
    struct mail_message *getInbox(char *owner, uint64_t index);

    struct mail *memory;
    std::vector<char *> accountIds;
    std::vector<struct mail_message *> messages;
};