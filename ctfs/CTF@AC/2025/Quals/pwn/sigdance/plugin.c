#include <stdint.h>

int verify(uint32_t provided, uint32_t ac, uint32_t uc, uint32_t pid) {
  uint32_t token = ((ac << 16) ^ (uc << 8) ^ (pid & 255u));
  return provided == token;
}
