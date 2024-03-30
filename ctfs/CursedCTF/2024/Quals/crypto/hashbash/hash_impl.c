#include<stdio.h>
#include<stdint.h>

uint32_t hash_djb2(unsigned char *str) {
	uint32_t hash = 5381; int c;
	while ((c = *str++)) {
		hash = ((hash << 5) + hash) + c;
    }
	return hash;
}

uint32_t hash_sdbm(unsigned char *str) {
    uint32_t hash = 0; int c;
    while ((c = *str++)) {
        hash = c + (hash << 6) + (hash << 16) - hash;
    }
    return hash;
}

uint32_t hash_loselose(unsigned char *str) {
    uint32_t hash = 0; int c;
    while ((c = *str++)) {
        hash += c;
    }
    return hash;
}

uint32_t hash_bkdr(unsigned char *str) {
    uint32_t hash = 0; int c;
    while ((c = *str++)) {
        hash = c + 31*hash;
    }
    return hash;
}

uint32_t hash_js(unsigned char *str) {
    uint32_t hash = 1315423911; int c;
    while ((c = *str++)) {
         hash = hash ^ ((hash << 5) + c + (hash >> 2));
    }
    return hash;
}
