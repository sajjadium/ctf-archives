#include <stdint.h>

class Memory;
struct mail;

class Service
{
public:
    Service(Memory *mem);
    ~Service();
    int SendMessage();
    void SendCreateAccount();
    void SendLoginAccount();
    void SendInbox();
    void SendDeleteMessage();
    void turnOff();
    void Logout();
    void handleError();
    bool ServiceDone();
    bool isLogin();

    char owner[33];
    struct mail *memory;
};
