#include "client_lib.h"
#include "util.h"

#include <err.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

void write_shared_file(char *filename, char *content, size_t content_len) {
  send_pid(BROKER_FD);
  send_ull(BROKER_FD, PUT_FILE);
  send_str(BROKER_FD, filename);
  send_ull(BROKER_FD, content_len);
  writen(BROKER_FD, content, content_len);
  char *resp = read_str(BROKER_FD);
  if (strcmp(resp, "OK") != 0) {
    err(1, "resp not OK");
  }
  free(resp);
}

int read_shared_file(char *filename) {
  send_pid(BROKER_FD);
  send_ull(BROKER_FD, GET_FILE);
  send_str(BROKER_FD, filename);
  send_str(BROKER_FD, filename);
  char *resp = read_str(BROKER_FD);
  if (strcmp(resp, "OK") != 0) {
    err(1, "resp not OK");
  }
  free(resp);
  open(filename, O_RDONLY);
}
