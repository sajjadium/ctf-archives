#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include "utils.h"
#include "ipc.h"

IPC *ipc_new(int fd, int proj_id) {
  IPC *ipc;
  key_t key;
  int shmid;
  IPC_packet *packet;
  char path[14 + 10];

  snprintf(path, sizeof(path), "/proc/self/fd/%d", fd);
  if ((key = ftok(path, proj_id)) == -1)
    return NULL;

  if ((shmid = shmget(key,
                      sizeof(IPC_packet) + IPC_MAX_SIZE,
                      IPC_CREAT | 0666)) < 0)
    return NULL;

  if ((packet = (IPC_packet*)shmat(shmid, NULL, 0)) == (IPC_packet*)-1) {
    shmctl(shmid, IPC_RMID, 0);
    return NULL;
  }

  if (!(ipc = (IPC*)malloc(sizeof(IPC)))) {
    shmctl(shmid, IPC_RMID, 0);
    return NULL;
  }

  ipc->shmid = shmid;
  ipc->panic = 0;
  ipc->src = -1;
  ipc->dst = -1;
  ipc->packet = packet;

  return ipc;
}

size_t ipc_recv(IPC *ipc, char *data, size_t len) {
  if (len > IPC_MAX_SIZE)
    fatal("Invalid size");

  do {
    while(!ipc->packet->ready)
      usleep(1337);
    usleep(1337);
  } while((ipc->packet->src == ipc->src)
          && (ipc->packet->dst == ipc->dst));

  if ((ipc->packet->src != ipc->dst)
      || (ipc->packet->dst != ipc->src)) {
    fatal("Invalid bridge (panic)");
  }

  memcpy(data, ipc->packet->data, len);

  ipc->packet->ready = 0;
  return len;
}

size_t ipc_send(IPC *ipc, const char *data, size_t len) {
  if (len > IPC_MAX_SIZE)
    fatal("Invalid size");

  do {
    while(ipc->packet->ready)
      usleep(1337);
    usleep(1337);
  } while((ipc->packet->src == -1)
          && (ipc->packet->dst == -1));

  memcpy(ipc->packet->data, data, len);
  ipc->packet->src = ipc->src;
  ipc->packet->dst = ipc->dst;
  ipc->packet->ready = 1;

  return len;
}

void ipc_bridge(IPC *ipc, pid_t src, pid_t dst) {
  ipc->src = src;
  ipc->dst = dst;
}

void ipc_delete(IPC *ipc) {
  shmdt(ipc->packet);
  shmctl(ipc->shmid, IPC_RMID, 0);
  free(ipc);
}
