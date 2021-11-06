#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>

#define PATH_MAX 0x100
#define REQUEST_MAX 0x100
#define RESPONSE_TEMPLATE(body)                   \
  "<!DOCTYPE html>\n"                             \
  "<html>\n"                                      \
  "  <head>\n"                                    \
  "    <meta charset=\"utf-8\">\n"                \
  "  </head>\n"                                   \
  "  <body>\n"                                    \
  "    <p>"body"</p>\n"                           \
  "  </body>\n"                                   \
  "</html>\n"

/**
 * Utility
 */
void recvline(int fd, char *buf, int size) {
  char c;

  memset(buf, 0, size);
  for (int i = 0; i != size; i++) {
    if (read(fd, &c, 1) <= 0) exit(1);
    if (c == '\r') {
      if (read(fd, &c, 1) <= 0) exit(1);
      if (c == '\n') {
        break;
      } else {
        buf[i] = '\r';
        buf[++i] = c;
      }
    } else {
      buf[i] = c;
    }
  }
}

void http_response(int fd, char *status, char *content, int length) {
  if (length < 0)
    length = strlen(content);

  dprintf(fd, "HTTP/1.1 %s\r\n", status);
  dprintf(fd, "Content-Length: %d\r\n", length);
  dprintf(fd, "Connection: close\r\n");
  dprintf(fd, "Content-Type: text/html; charset=UTF-8\r\n\r\n");
  write(fd, content, length);
}

/**
 * HTTP server
 */
void http_saba(int sock) {
  char *p;
  char path[PATH_MAX];
  char request[REQUEST_MAX+1];
  struct stat st;

  /* Receive request header */
  recvline(sock, request, REQUEST_MAX);

  /* Check request method */
  p = strtok(request, " ");
  if (memcmp(p, "GET", 3) != 0) {
    http_response(sock, "405 Method Not Allowed",
                  RESPONSE_TEMPLATE("404 Method Not Allowed 🙅‍️"), -1);
    return;
  }

  /* Check path */
  p = strtok(NULL, " ");
  if (p[0] != '/') {
    http_response(sock, "400 Bad Request",
                  RESPONSE_TEMPLATE("400 Bad Request 🤮"), -1);
    return;
  }
  if (strstr(p, "..")) {
    http_response(sock, "451 Unavailable For Legal Reasons",
                  RESPONSE_TEMPLATE("451 Hacking Attempt 👮"), -1);
    return;
  }

  /* Check file */
  strcpy(path, "./html");
  if (p[1] == '\0')
    strncat(path, "/index.html", PATH_MAX-1);
  else
    strncat(path, p, PATH_MAX-1);

  if (stat(path, &st) != 0) {
    http_response(sock, "404 Not Found",
                  RESPONSE_TEMPLATE("404 Not Found 🔍"), -1);
    return;
  }

  /* Read file */
  char *content = calloc(sizeof(char), st.st_size);
  if (content == NULL) {
    http_response(sock, "500 Internal Server Error",
                  RESPONSE_TEMPLATE("500 Internal Server Error 😇"), -1);
    return;
  }

  int fd = open(path, O_RDONLY);
  if (fd < 0) {
    free(content);
    http_response(sock, "500 Internal Server Error",
                  RESPONSE_TEMPLATE("500 Internal Server Error 😇"), -1);
    return;
  }
  read(fd, content, st.st_size);

  /* Make response */
  http_response(sock, "200 OK",
                content, st.st_size);
  free(content);
}

/**
 * Entry point
 */
int main() {
  int sockfd, yes=1;
  struct sockaddr_in server_addr;

  if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
    perror("socket");
    exit(1);
  }

  memset(&server_addr, 0, sizeof(server_addr));
  server_addr.sin_family = AF_INET;
  server_addr.sin_addr.s_addr = INADDR_ANY;
  server_addr.sin_port = htons(9080);

  if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (const char*)&yes, sizeof(yes)) < 0) {
    perror("setsockopt");
    exit(1);
  }

  if (bind(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
    perror("bind");
    close(sockfd);
    exit(1);
  }

  if (listen(sockfd, 10)) {
    perror("listen");
    close(sockfd);
    exit(1);
  }

  while (1) {
    int fd, client_len, pid, cpid, status;
    struct sockaddr_in client_addr;

    client_len = sizeof(client_addr);
    if ((fd = accept(sockfd, (struct sockaddr*)&client_addr, &client_len)) < 0) {
      perror("accept");
      exit(1);
    }

    pid = fork();
    if (pid == -1) {
      perror("fork");
      exit(1);
    } else if (pid == 0) {
      /* HTTP server */
      alarm(30);
      http_saba(fd);
      exit(0);
    } else {
      while ((cpid = waitpid(-1, &status, WNOHANG)) > 0);
      if (cpid < 0 && errno != ECHILD) {
        perror("waitpid");
        exit(1);
      }
    }
    close(fd);
  }
}
