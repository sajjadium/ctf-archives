#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/random.h>
#include "utils.h"
#include "auth.h"

int username_validator(const char *authdir, IPC *ipc) {
  char username[32];
  ipc_recv(ipc, username, 32);
  return fscmp(authdir, "username", username);
}
void username_reader(IPC *ipc) {
  char username[32];
  printf("Username: ");
  if (scanf("%s", username) != 1) exit(1);
  ipc_send(ipc, username, strlen(username) + 1);
}

int password_validator(const char *authdir, IPC *ipc) {
  char password[32];
  ipc_recv(ipc, password, 32);
  return fscmp(authdir, "password", password);
}
void password_reader(IPC *ipc) {
  char password[32];
  printf("Password: ");
  if (scanf("%31s", password) != 1) exit(1);
  ipc_send(ipc, password, strlen(password) + 1);
}

int token_validator(const char *authdir, IPC *ipc) {
  char token[24], result[32];
  rndstr(token, 24);
  //
  // [WIP] Send this token to the user's SMS
  //
  ipc_send(ipc, token, 24);
  ipc_recv(ipc, result, 3);
  return strcmp(result, "OK");
}
void token_reader(IPC *ipc) {
  char token[24], buf[32];
  ipc_recv(ipc, token, 24);
  printf("Token: ");
  if (scanf("%31s", buf) != 1) exit(1);
  if (memcmp(token, buf, 24) == 0) {
    ipc_send(ipc, "OK", 3);
  } else {
    ipc_send(ipc, "NG", 3);
  }
}

int authenticator(const char *authdir,
                  AUTH_VALIDATOR validator,
                  AUTH_READER reader) {
  IPC *ipc;
  int status, auth, fd, key;
  pid_t pid;

  if (((fd = memfd_create(".ipc", 0)) == -1)
      || (getrandom(&key, sizeof(int), 0) != sizeof(int))) {
    fatal("Failed to generate IPC key");
  }

  if ((pid = fork()) == -1) {

    fatal("Failed to fork");

  } else if (pid == 0) {
    alarm(60);

    if (!(ipc = ipc_new(fd, key))) {
      fatal("Failed to initialize IPC");
    }
    ipc_bridge(ipc, getpid(), getppid());

    sandboxify();
    (*reader)(ipc);

    ipc_delete(ipc);
    close(fd);
    exit(0);

  }

  if (!(ipc = ipc_new(fd, key))) {
    fatal("Failed to initialize IPC");
  }
  ipc_bridge(ipc, getpid(), pid);

  auth = (*validator)(authdir, ipc);
  wait(&status);
  if (status != 0)
    return -1;

  ipc_delete(ipc);
  close(fd);
  return auth;
}
