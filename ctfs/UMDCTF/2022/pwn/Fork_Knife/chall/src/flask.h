#include <sys/types.h>

#define MAX_ARGC 16
#define MAX_ARGLEN 256
#define MAX_REQ (sizeof(struct request) + 256)

#define CMD_ADD 0
#define CMD_MIX 1

struct request {
    char cmd;
    char idx;
    char len;    // optional
    char arg[0]; // optional
};

extern int num_flasks;

void init_flasks(int n);
void clean_flasks(void);
void flask_add(int id, int i, const char *arg, size_t n);
void flask_mix(int id);
void flask_empty(int id);
