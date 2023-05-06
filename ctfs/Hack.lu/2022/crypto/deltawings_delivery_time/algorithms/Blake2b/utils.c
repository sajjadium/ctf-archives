#include "utils.h"

/**
 * @brief      Helper function to perform rotation in a 64 bit int
 *
 * @param[in]  w     original word
 * @param[in]  c     offset to rotate by
 *
 * @return     The rotated result
 */
uint64_t
rotr64(const uint64_t w, const unsigned c)
{
  return (w >> c) | (w << (64 - c));
}

/**
 * @brief      Loads into src 64 bytes at a time
 *
 * @param[in]  src   The source
 *
 * @return     { description_of_the_return_value }
 */
uint64_t
load64(const void* src)
{
#if defined(NATIVE_LITTLE_ENDIAN)
  uint64_t w;
  memcpy(&w, src, sizeof w);
  return w;
#else
  const uint8_t* p = (const uint8_t*)src;
  return ((uint64_t)(p[0]) << 0) | ((uint64_t)(p[1]) << 8) |
         ((uint64_t)(p[2]) << 16) | ((uint64_t)(p[3]) << 24) |
         ((uint64_t)(p[4]) << 32) | ((uint64_t)(p[5]) << 40) |
         ((uint64_t)(p[6]) << 48) | ((uint64_t)(p[7]) << 56);
#endif
}

/**
 * @brief      Stores w into dst
 *
 * @param      dst   The destination
 * @param[in]  w     word to be stored
 */
void
store64(void* dst, uint64_t w)
{
#if defined(NATIVE_LITTLE_ENDIAN)
  memcpy(dst, &w, sizeof w);
#else
  uint8_t* p = (uint8_t*)dst;
  p[0] = (uint8_t)(w >> 0);
  p[1] = (uint8_t)(w >> 8);
  p[2] = (uint8_t)(w >> 16);
  p[3] = (uint8_t)(w >> 24);
  p[4] = (uint8_t)(w >> 32);
  p[5] = (uint8_t)(w >> 40);
  p[6] = (uint8_t)(w >> 48);
  p[7] = (uint8_t)(w >> 56);
#endif
}

void
store32(void* dst, uint32_t w)
{
#if defined(NATIVE_LITTLE_ENDIAN)
  memcpy(dst, &w, sizeof w);
#else
  uint8_t* p = (uint8_t*)dst;
  p[0] = (uint8_t)(w >> 0);
  p[1] = (uint8_t)(w >> 8);
  p[2] = (uint8_t)(w >> 16);
  p[3] = (uint8_t)(w >> 24);
#endif
}

/**
 * @brief      increments the blake2b state counter
 *
 * @param      S     blake2b_state instance
 * @param[in]  inc   The increment
 */
void
blake2b_increment_counter(blake2b_state* S, const uint64_t inc)
{
  S->t[0] += inc;
  S->t[1] += (S->t[0] < inc);
}
