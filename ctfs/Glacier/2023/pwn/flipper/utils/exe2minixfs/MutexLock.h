// WARNING: You are looking for a different MutexLock.h - this one is just for the exe2minixfs tool!

#ifdef EXE2MINIXFS
#pragma once

class Mutex;

class MutexLock
{
public:
    MutexLock(Mutex &){};
    MutexLock(Mutex &, bool){};

    MutexLock(MutexLock const&) = delete;
    MutexLock &operator=(MutexLock const&) = delete;
};
#endif
