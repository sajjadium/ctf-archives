#ifndef __BABYAUTH_IPC__
#define __BABYAUTH_IPC__

#include <sys/types.h>
#define IPC_MAX_SIZE 0x100

typedef struct {
  int ready;
  pid_t src;
  pid_t dst;
  char data[1];
} IPC_packet;

typedef struct {
  int shmid;
  int panic;
  pid_t src;
  pid_t dst;
  IPC_packet *packet;
} IPC;

IPC *ipc_new(int fd, int proj_id);
void ipc_bridge(IPC *ipc, pid_t src, pid_t dst);
size_t ipc_recv(IPC *ipc, char *data, size_t len);
size_t ipc_send(IPC *ipc, const char *data, size_t len);
void ipc_delete(IPC *ipc);

#endif
