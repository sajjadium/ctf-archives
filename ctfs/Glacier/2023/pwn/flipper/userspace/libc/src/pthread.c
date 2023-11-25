#include "pthread.h"

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_create(pthread_t *thread, const pthread_attr_t *attr,
                   void *(*start_routine)(void *), void *arg)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
void pthread_exit(void *value_ptr)
{
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_cancel(pthread_t thread)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_join(pthread_t thread, void **value_ptr)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_detach(pthread_t thread)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_mutex_destroy(pthread_mutex_t *mutex)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_mutex_lock(pthread_mutex_t *mutex)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_mutex_unlock(pthread_mutex_t *mutex)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_cond_init(pthread_cond_t *cond, const pthread_condattr_t *attr)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_cond_destroy(pthread_cond_t *cond)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_cond_signal(pthread_cond_t *cond)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_cond_broadcast(pthread_cond_t *cond)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_spin_destroy(pthread_spinlock_t *lock)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_spin_init(pthread_spinlock_t *lock, int pshared)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_spin_lock(pthread_spinlock_t *lock)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_spin_trylock(pthread_spinlock_t *lock)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_spin_unlock(pthread_spinlock_t *lock)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_setcancelstate(int state, int *oldstate)
{
  return -1;
}

/**
 * function stub
 * posix compatible signature - do not change the signature!
 */
int pthread_setcanceltype(int type, int *oldtype)
{
  return -1;
}

