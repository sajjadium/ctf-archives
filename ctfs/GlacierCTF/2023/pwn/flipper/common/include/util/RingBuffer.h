#pragma once

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef __cplusplus
}
#endif

#include "new.h"
#include "ArchThreads.h"
#include "assert.h"

template<class T>
class RingBuffer
{
  public:
    RingBuffer ( uint32 size=128 );
    ~RingBuffer();
    bool get ( T &c );
    void put ( T c );
    void clear();

  private:

    size_t buffer_size_;
    T *buffer_;
    size_t write_pos_;
    size_t read_pos_;
};

template <class T>
RingBuffer<T>::RingBuffer ( uint32 size )
{
  assert ( size>1 );
  buffer_size_=size;
  buffer_=new T[buffer_size_];
  write_pos_=1;
  read_pos_=0;
}

template <class T>
RingBuffer<T>::~RingBuffer()
{
  delete[] buffer_;
}

template <class T>
void RingBuffer<T>::put ( T c )
{
  size_t old_write_pos=write_pos_;
  if ( old_write_pos == read_pos_ )
    return;
  buffer_[old_write_pos]=c;
  ArchThreads::testSetLock ( write_pos_, ( old_write_pos + 1 ) % buffer_size_ );
}

template <class T>
void RingBuffer<T>::clear()
{
  ArchThreads::testSetLock ( write_pos_,1 );
  // assumed that there is only one reader who can't have called clear and get at the same time.
  // here get would return garbage.
  ArchThreads::testSetLock ( read_pos_,0 );
}

template <class T>
bool RingBuffer<T>::get ( T &c )
{
  uint32 new_read_pos = ( read_pos_ + 1 ) % buffer_size_;
  if ( write_pos_ == new_read_pos ) //nothing new to read
    return false;
  c = buffer_[new_read_pos];
  ArchThreads::testSetLock ( read_pos_,new_read_pos );
  return true;
}

