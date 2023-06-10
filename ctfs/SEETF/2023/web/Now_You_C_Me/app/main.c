#include "httpd.h"
#include <sys/stat.h>

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define CHUNK_SIZE 1024 // read 1024 bytes at a time

// Public directory settings
#define PUBLIC_DIR "./public"
#define INDEX_HTML "/index.html"
#define NOT_FOUND_HTML "/404.html"

bool is_admin = false;

int main(int c, char **v) {
  char *port = c == 1 ? "80" : v[1];
  serve_forever(port);
  return 0;
}

int file_exists(const char *file_name) {
  struct stat buffer;
  int exists;

  exists = (stat(file_name, &buffer) == 0);

  return exists;
}

int read_file(const char *file_name) {
  char buf[CHUNK_SIZE];
  FILE *file;
  size_t nread;
  int err = 1;

  file = fopen(file_name, "r");

  if (file) {
    while ((nread = fread(buf, 1, sizeof buf, file)) > 0)
      fwrite(buf, 1, nread, stdout);

    err = ferror(file);
    fclose(file);
  }
  return err;
}

void route() {

  if (request_header("Authorization") != NULL && strcmp(request_header("Authorization"), getenv("SECRET")) == 0) {
    is_admin = true;
  }

  ROUTE_START()
  
  GET("/") {
    char index_html[20];
    sprintf(index_html, "%s%s", PUBLIC_DIR, INDEX_HTML);

    HTTP_200;
    PUBLIC_RESPONSE_HEADERS;
    if (file_exists(index_html)) {
      read_file(index_html);
    } else {
      printf("Hello! You are using %s\n\n", request_header("User-Agent"));
    }
  }

  GET("/api/health") {
    if (!is_admin) {
      HTTP_401;
      API_UNAUTHORIZED_HEADERS;
      printf("{\"error\": \"%s\"}", "You are not authorized to access this resource");
      return;
    }

    HTTP_200;
    API_RESPONSE_HEADERS;
    printf("{\"status\": \"%s\"}", "OK");
  }

  POST("/api/flag") {

    if (getenv("SECRET") == NULL || getenv("FLAG") == NULL) {
      HTTP_500;
      API_RESPONSE_HEADERS;
      printf("Flag not found, please contact admins.");
      return;
    }

    if (
      request_header("Origin") == NULL || request_header("Host") == NULL || strlen(request_header("Origin")) <= 7 ||
      strcmp(request_header("Origin") + 7, request_header("Host")) != 0
    ) {
      HTTP_401;
      API_RESPONSE_HEADERS;
      printf("{\"error\": \"%s\"}", "CSRF detected!");
      return;
    }
    
    if (!is_admin) {
      HTTP_401;
      API_UNAUTHORIZED_HEADERS;
      printf("{\"error\": \"%s\"}", "You are not authorized to access this resource");
      return;
    }

    HTTP_200;
    API_RESPONSE_HEADERS;
    printf("{\"flag\": \"%s\"}", getenv("FLAG"));
  }

  ROUTE_END()
}