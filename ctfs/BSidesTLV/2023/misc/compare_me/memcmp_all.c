#include <stdint.h>

// Constant-Time memcmp implementation to avoid side-channels

uint32_t memcmp_all(const void *p1, const void *p2, uint32_t compare_len) {
  uint32_t result = 0;

  uint32_t *pDW1 = (uint32_t *)p1;
  uint32_t *pDW2 = (uint32_t *)p2;
  uint8_t *pByte1;
  uint8_t *pByte2;

  while (compare_len >= sizeof(int)) {
    result |= (*pDW1 ^ *pDW2);
    pDW1++;
    pDW2++;
    compare_len -= sizeof(int);
  }

  pByte1 = (uint8_t *)pDW1;
  pByte2 = (uint8_t *)pDW2;

  while (compare_len > 0) {
    result |= (uint32_t)(*pByte1 ^ *pByte2);
    pByte1++;
    pByte2++;
    compare_len--;
  }

  return result;
}
