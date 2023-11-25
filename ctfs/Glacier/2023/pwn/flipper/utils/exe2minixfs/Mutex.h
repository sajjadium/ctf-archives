// WARNING: You are looking for a different Mutex.h - this one is just for the exe2minixfs tool!
#ifdef EXE2MINIXFS
#pragma once

class Mutex
{
public:

  Mutex(const char*){};

  Mutex(Mutex const &) = delete;
  Mutex &operator=(Mutex const&) = delete;

  bool acquireNonBlocking(pointer = 0){return true;};

  void acquire(pointer = 0){};
  void release(pointer = 0){};

  bool isFree(){ return true; };
};

#endif
