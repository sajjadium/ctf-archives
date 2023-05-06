#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>
#include "redis.h"

void show_banner(int port, int pid) {
  if (!getenv("REDIS_QUIET")) {
    printf("     _\n"
           " .-``@''-.  Redis-Lite 1.0.0 64 bit\n"
           "(  @   @  )\n"
           "|`--._.--'| Running in stand alone mode\n"
           "|`-.._..-'| Port: %d\n"
           " `-.___.-'  PID: %d\n\n", port, pid);
  }
}

int main(int argc, char **argv, char **envp)
{
  int port, sock_server, sock_client, pid, y = 1;
  unsigned len;
  char *str_port;
  struct sockaddr_in server, client;

  /* Set port number */
  if (str_port = getenv("REDIS_PORT")) {
    port = atoi(str_port);
  } else {
    port = 6379;
  }

  /* Setup socket */
  if ((sock_server = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
    perror("socket");
    return 1;
  }

  server.sin_family = AF_INET;
  server.sin_port = htons(port);
  server.sin_addr.s_addr = INADDR_ANY;
  setsockopt(sock_server, SOL_SOCKET, SO_REUSEADDR,
             (const char*)&y, sizeof(y));

  if (bind(sock_server, (struct sockaddr*)&server, sizeof(server))) {
    perror("bind");
    return 1;
  }

  show_banner(port, getpid());
  listen(sock_server, 8);

  while (1) {
    /* Establish connection */
    len = sizeof(client);
    if ((sock_client = accept(sock_server,
                              (struct sockaddr*)&client, &len)) < 0) {
      perror("accept");
      exit(1);
    }

    /* Fork redis-lite-server */
    pid = fork();
    if (pid == 0) {
      printf("[+] New connection from %s:%d (%d)\n",
             inet_ntoa(client.sin_addr), ntohs(client.sin_port), getpid());
      redis_server_run(sock_client);
      close(sock_client);
      exit(0);

    } else if (pid == -1) {
      perror("fork");
      exit(1);
    }
    close(sock_client);

    /* Kill zombies */
    while((pid = wait4(-1, 0, WNOHANG, 0)) > 0);
  }

  close(sock_server);
  return 0;
}
