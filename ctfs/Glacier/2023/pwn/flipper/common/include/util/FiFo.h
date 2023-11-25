#pragma once

#include "kprintf.h"
#include "new.h"
#include "Mutex.h"
#include "Condition.h"

#ifdef __cplusplus
extern "C"
{
#endif

#ifdef __cplusplus
}
#endif

#define FIFO_NOBLOCK_PUT 1
#define FIFO_NOBLOCK_PUT_OVERWRITE_OLD 2

template<class T>
class FiFo
{
  public:

    /**
     * Constructor
     * @param inputb_size the buffer size (default 512)
     * @param flags FIFO_NOBLOCK_PUT or FIFO_NOBLOCK_PUT_OVERWRITE_OLD (default none)
     * @return
     */
    FiFo(uint32 inputb_size = 512, uint8 flags = 0);

    ~FiFo();

    /**
     * Puts the given parameter in the fifo buffer.
     * @param c the parameter to put
     */
    void put(T c);

    /**
     * Returns a element from the fifo buffer
     * @return the element
     */
    T get();

    /**
     * Returns if there is a next element in the buffer and stores it in the given parameter.
     * @param c the paramter to store the element in
     * @return true if there is a next element
     */
    bool peekAhead(T &c);

    /**
     * Returns the number of elements in the fifo buffer.
     * @return the number of elements
     */
    uint32 countElementsAhead();

    void clear();

  private:
    Mutex input_buffer_lock_;
    Condition something_to_read_;
    Condition space_to_write_;

    uint32 input_buffer_size_;
    T *input_buffer_;
    uint32 ib_write_pos_;
    uint32 ib_read_pos_;

    uint8 flags_;
};

template<class T>
FiFo<T>::FiFo(uint32 inputb_size, uint8 flags) :
    input_buffer_lock_("FiFo input_buffer_lock_"), something_to_read_(&input_buffer_lock_, "FiFo::something_to_read_"),
	space_to_write_(&input_buffer_lock_, "FiFo::space_to_write_")
{
  if (inputb_size < 2)
    input_buffer_size_ = 512;
  else
    input_buffer_size_ = inputb_size;

  input_buffer_ = new T[input_buffer_size_];
  ib_write_pos_ = 1;
  ib_read_pos_ = 0;
  flags_ = flags;
}

template<class T>
FiFo<T>::~FiFo()
{
  delete[] input_buffer_;
}

//only put uses the fallback buffer -> so it doesn't need a lock
//input_buffer could be in use -> so if locked use fallback
template<class T>
void FiFo<T>::put(T c)
{
  input_buffer_lock_.acquire();
  if (ib_write_pos_ == ib_read_pos_)
  {
    if (flags_ & FIFO_NOBLOCK_PUT)
    {
      if (flags_ & FIFO_NOBLOCK_PUT_OVERWRITE_OLD)
        ib_read_pos_ = (ib_read_pos_ + 1) % input_buffer_size_; //move read pos ahead of us
      else
      {
        input_buffer_lock_.release();
        return;
      }
    }
    else
      while (ib_write_pos_ == ib_read_pos_)
        space_to_write_.wait();
  }
  something_to_read_.signal();
  input_buffer_[ib_write_pos_++] = c;
  ib_write_pos_ %= input_buffer_size_;
  input_buffer_lock_.release();
}

template<class T>
void FiFo<T>::clear(void)
{
  input_buffer_lock_.acquire();
  ib_write_pos_ = 1;
  ib_read_pos_ = 0;
  input_buffer_lock_.release();
}

//now this routine could get preempted
template<class T>
T FiFo<T>::get()
{
  T ret = 0;
  input_buffer_lock_.acquire();

  while (ib_write_pos_ == ((ib_read_pos_ + 1) % input_buffer_size_)) //nothing new to read
    something_to_read_.wait(); //this implicates release & acquire

  space_to_write_.signal();
  ib_read_pos_ = (ib_read_pos_ + 1) % input_buffer_size_;
  ret = input_buffer_[ib_read_pos_];

  input_buffer_lock_.release();
  return ret;
}

//now this routine could get preempted
template<class T>
bool FiFo<T>::peekAhead(T &ret)
{
  input_buffer_lock_.acquire();

  if (ib_write_pos_ == ((ib_read_pos_ + 1) % input_buffer_size_)) //nothing new to read
  {
    input_buffer_lock_.release();
    return false;
  }

  ret = input_buffer_[(ib_read_pos_ + 1) % input_buffer_size_];
  input_buffer_lock_.release();
  return true;
}

template<class T>
uint32 FiFo<T>::countElementsAhead()
{
  input_buffer_lock_.acquire();
  uint32 count = ib_write_pos_ - ib_read_pos_;
  input_buffer_lock_.release();
  if (count == 0)
    return input_buffer_size_;
  else if (count > 0)
    return (count - 1);
  else
    // count < 0
    return (input_buffer_size_ + count);
}

