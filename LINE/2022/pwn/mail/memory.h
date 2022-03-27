#include <sys/ipc.h>
#include <sys/shm.h>

class Memory
{
public:
    Memory(key_t id);
    ~Memory();
    void createShMemory();
    void *getShMemory();

    int shmId;
    key_t keyId;
    void *memory;
};