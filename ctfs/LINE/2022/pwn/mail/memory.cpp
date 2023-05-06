#include <cstdlib>
#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <string.h>

#include "memory.h"

Memory::Memory(key_t id) : keyId(id), shmId(0)
{
}

Memory::~Memory()
{
    keyId = 0;
    shmId = 0;
    shmdt(memory);
}

void Memory::createShMemory()
{
    shmId = shmget(keyId, 0x1000, 0666 | IPC_CREAT);
    if (shmId == -1)
    {
        std::cout << "[-] Failed to get identifier" << std::endl;
        exit(0);
    }

    memory = shmat(shmId, (void *)0, 0);
    if (memory == (void *)-1)
    {
        std::cout << "[-] Failed to allocate" << std::endl;
        exit(0);
    }

    bzero(memory, 0x1000);
}

void *Memory::getShMemory()
{
    return memory;
}