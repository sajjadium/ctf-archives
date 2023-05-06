#include <sys/types.h>

#define SANDBOX_FD 29
#define BROKER_FD 30

#define GET_FILE 0
#define PUT_FILE 1
#define EXIT 2

void copy_fd(int in, int out);
void copy_fd_len(int in, int out, size_t len);
int create_under_root(const char *root, const char *path);

void make_cloexec(int fd);

ssize_t check(ssize_t ret, const char * const msg);
void die(const char *msg);
void *check_malloc(size_t size);
void readn(int fd, void *buf, size_t len);
void writen(int fd, const void *buf, size_t len);

char *read_str(int fd);
void send_str(int chan, const char *s);
unsigned long long read_ull(int fd);
void send_ull(int chan, unsigned long long l);

void send_fd(int chan, int fd);
int recv_fd(int chan);

void send_pid(int chan);
int recv_pid(int chan);
