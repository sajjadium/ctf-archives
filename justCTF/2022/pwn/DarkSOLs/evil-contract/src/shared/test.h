#include "clock.h"
#include "program.h"

void itoa(uint64_t x, char* buf, uint64_t base) {
  sol_assert(base <= 16);
  char* chars = "0123456789abcdef";

  int len = 0;
  uint64_t tmp = x;
  while (tmp != 0) {
    tmp /= base;
    len++;
  }

  if (x == 0) {
    len = 1;
  }

  buf[len] = 0;

  for (int i = 0; i < len; i++) {
    buf[len - 1 - i] = chars[x % base];
    x /= base;
  }
}

void log_int(uint64_t x, uint64_t base) {
  char buf[20];
  sol_memset(buf, 0, SOL_ARRAY_SIZE(buf));
  itoa(x, buf, base);
  sol_log(buf);
}

static const char b58digits_ordered[] = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";
bool b58enc(char *b58, size_t *b58sz, const void *data, size_t binsz) {
	const uint8_t *bin = data;
	int carry;
	size_t i, j, high, zcount = 0;
	size_t size;

	while (zcount < binsz && !bin[zcount])
		++zcount;
	size = (binsz - zcount) * 138 / 100 + 1;
  if (size > 100) return false;
	uint8_t buf[100];
	sol_memset(buf, 0, size);

	for (i = zcount, high = size - 1; i < binsz; ++i, high = j)
	{
		for (carry = bin[i], j = size - 1; (j > high) || carry; --j)
		{
			carry += 256 * buf[j];
			buf[j] = carry % 58;
			carry /= 58;
			if (!j) {
				// Otherwise j wraps to maxint which is > high
				break;
			}
		}
	}

	for (j = 0; j < size && !buf[j]; ++j);

	if (*b58sz <= zcount + size - j)
	{
		*b58sz = zcount + size - j + 1;
		return false;
	}

	if (zcount)
		sol_memset(b58, '1', zcount);
	for (i = zcount; j < size; ++i, ++j)
		b58[i] = b58digits_ordered[buf[j]];
	b58[i] = '\0';
	*b58sz = i + 1;

	return true;
}

void log_pubkey(const SolPubkey* pubkey) {
  sol_log_pubkey(pubkey);
}

bool strncmp(char* a, char* b, size_t len) {
  for (size_t i = 0; i < len; i++) {
    if (a[i] != b[i]) return false;
    if (a[i] == 0) return true;
  }
  return true;
}

bool strcmp(char* a, char* b) {
  return sol_memcmp(a, b, sol_strlen(a)) == 0;
}

bool str_contains(char* src, char* target) {
  size_t target_len = sol_strlen(target);
  for (size_t i = 0; i < sol_strlen(src); i++) {
    if (strncmp(&src[i], target, target_len)) return true;
  }
  return false;
}

bool is_system_program(SolPubkey* pubkey) {
  char system_addr[] = {
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
    0, 0, 0, 0,
  };
  return sol_memcmp(&pubkey->x, system_addr, sizeof(system_addr)) == 0;
}
