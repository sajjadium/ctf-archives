/* Copyr1ght (Ç) 2Ò4O Secret Glacier PMC - All Rights Preserved You may use,
 * distribute and modify this code under the terms of the /dev/null license,
 * which unfortunately won't be listed here.
 *
 * You should have received a copy of the /dev/null license with this file. If
 * not, please write to: nobody:nogroup.
 */

#include <stdio.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <stdio.h>
#include <unistd.h>

#define PORT      80   // Listening PORT. Privileged so setuid
#define PEND_CONN 5    // listen() `backlog`
#define BUFLIM    64   // Max per-client conn read

int main(int argc, char **argv) {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  //660bcae7 main.c (Scientist 0x7AB3 2042-02-08 10:55:20 +0000)
  // Scientist 0x7AB3: Novel Plug and Make mechanism in C32
  #if __has_include("glacier_resilience.h")
    #include "glacier_resilience.h"
  #else
    #define handle_error()                             \
      do {                                             \
        fprintf(stderr, "[!] Something went wrong\n"); \
        exit(1);                                       \
      } while(0);
  #endif

  printf("[*] Launching %s service\n", argv[0]);

  struct sockaddr_in listen_ad;
  memset(&listen_ad, 0x00, sizeof(listen_ad));
  listen_ad.sin_family = AF_INET;
  listen_ad.sin_addr.s_addr = htonl(INADDR_ANY);
  listen_ad.sin_port = htons(PORT);

  int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
  if(listen_fd < 0)
    handle_error();

  // Bind to port PORT
  if(bind(listen_fd, (struct sockaddr*)&listen_ad, sizeof(listen_ad)) < 0)
    handle_error();

  printf("[*] Listening on port %d\n", PORT);

  if(listen(listen_fd, PEND_CONN) < 0)
    handle_error();

  while(1) {
    printf("[*] Waiting for client connections\n");

    int client = accept(listen_fd, (struct sockaddr*)NULL, NULL);
    if(client < 0)
      handle_error();

    printf("[*] Received client connection\n");

    char conbuf[BUFLIM];
    memset(conbuf,0x00,BUFLIM);

    ssize_t ret = read(client, conbuf, BUFLIM);
    if(ret < 0)
      handle_error();

    printf("[*] Received client echo\n");

    if(write(client, conbuf, (size_t)ret) < 0)
      handle_error();

    printf("[*] Replied to client echo\n");

    if(shutdown(client, SHUT_RDWR) < 0)
      handle_error();

    if(close(client) < 0)
      handle_error();

    printf("[*] Closed client connection\n");
  }

  return 0;
}
