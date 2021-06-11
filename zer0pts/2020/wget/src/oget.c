#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <netdb.h>
#include <netinet/in.h>
#include <sys/param.h>
#include <ctype.h>
#include <unistd.h>
#include "oget.h"

int depth = 0;

/** fatal
 * Print error message and exit
 */
_Noreturn void fatal(char *msg) {
  fprintf(stderr, "[ABORT] %s\n", msg);
  exit(1);
}

/** readline
 * Read until newline ('\r\n')
 */
int readline(int sock, char *buf, int len) {
  int i;
  char *ptr;
  memset(buf, 0, len);
  for(ptr = buf, i = 0; read(sock, ptr, 1) > 0; ptr++, i++) {
    if (*(ptr - 1) == '\r' && *ptr == '\n') {
      *(ptr - 1) = *ptr = '\0';
      return 0;
    }
    if (i >= len) return 2;
  }
  fatal("Connection closed");
}

/** validate_url
 * Check if URL starts with 'http://'
 */
int validate_url(char *url) {
  if (*(unsigned int*)url != 0x70747468
      || url[4] != ':'
      || url[5] != '/'
      || url[6] != '/') {
    return 1;
  }
  return 0;
}

/** split_url
 * Split URL into host and path
 */
void split_url(char *url, char **host, char **port, char **path) {
  /* skip 'http://' */
  *host = &url[7];

  /* retrieve path */
  *path = strchr(*host, '/');
  if (*path == NULL) {
    /* there's no path (i.e. 'http://example.com') */
    *path = &url[strlen(url)];
  } else {
    /* remove root '/' */
    **path = '\0';
    ++(*path);
  }

  if (strchr(*host, '@')) {
    /* i.e. 'http://user:pass@example.com/' */
    fatal("Auth request is not implemented");
  }

  /* retrieve port number */
  *port = strchr(*host, ':');
  if (*port == NULL) {
    /* use http if no port number is specified */
    *port = malloc(8);
    strcpy(*port, "80");
  } else {
    /* remove colon */
    **port = '\0';
    ++(*port);
  }
}

/** parse_response
 * Split response header into key and value
 */
void parse_response(char *response, char **key, char **value) {
  char *ptr;
  *key = *value = NULL;

  *value = strchr(response, ':');
  if (*value) {
    *key = response;
    **value = '\0';  /* remove colon */
    (*value) += 2;   /* skip whitespace after colon */

    /* lowercase key */
    for(ptr = *key; *ptr; ptr++) *ptr = tolower(*ptr);
  }
}

/** download_file
 * Send HTTP request and receive the result
 */
char *download_file(char *host, char *port, char *path) {
  int sock;
  unsigned long length;
  struct addrinfo server, *res;
  struct in_addr addr;
  char *key, *value;
  char *request, *response, *html, *redirect;

  request = response = html = redirect = NULL;

  /* establish connection */
  memset(&server, 0, sizeof(server));
  server.ai_socktype = SOCK_STREAM;
  server.ai_family   = AF_INET;
  if (getaddrinfo(host, port, &server, &res) != 0) {
    fatal("Could not resolve hostname");
  }

  if ((sock = socket(res->ai_family, res->ai_socktype, res->ai_protocol)) < 0) {
    fatal("Could not create socket");
  }

  if (connect(sock, res->ai_addr, res->ai_addrlen) != 0) {
    fatal("Could not connect to host");
  }

  /* send HTTP request */
  request = malloc(SIZE_HEADER + strlen(path) + strlen(host) + 1);
  sprintf(request, "GET /%s HTTP/1.1\r\nHost: %s:%s\r\n\r\n", path, host, port);
  write(sock, request, strlen(request));

  /* receive HTTP response */
  response = malloc(SIZE_RESPONSE);
  while (1) {
    if (readline(sock, response, SIZE_RESPONSE)) {
      /* Skip too long request */
      continue;
    }

    if (*response == '\0') {
      /* end of response headers */
      break;
    }

    /* parse response header */
    parse_response(response, &key, &value);
    if (key == NULL || value == NULL) {
      continue;
    }

    if (strcmp(key, "location") == 0) {
      /* validate URL */
      if (!validate_url(value) || value[0] == '/') {
        /* follow redirects */
        redirect = malloc(strlen(value) + 1);
        memcpy(redirect, value, strlen(value));
        
        /* no longer need html */
        if (html) free(html);
      } else {
        /* location value is neither URL nor path */
        fatal("Redirected URL must start with 'http://' or '/'");
      }
    } else if (strcmp(key, "content-length") == 0) {
      /* allocate buffer for html */
      length = atol(value);
      html = malloc(length + 1);
      if (html == NULL) fatal("Memory error");
    }
  }

  free(request);
  free(response);

  if (redirect) {
    /* support for omitted hostname */
    if (redirect[0] == '/') {
      char *t = malloc(SIZE_HOST + strlen(host) + strlen(redirect) + 1);
      sprintf(t, "http://%s:%s%s", host, port, redirect);
      free(redirect);
      redirect = t;
    }
    
    /* redirect to the new URL and return it's HTML */
    close(sock);
    return omega_get(redirect);
    
  } else {
    /* read HTML */
    if (html && length > 0) {
      if (read(sock, html, length) == 0) {
        fatal("Connection closed");
      }
    } else {
      fatal("Empty response");
    }
    
    close(sock);
    return html;
  }
}

/** omega_get
 * Access to URL and return HTML code
 */
char *omega_get(char *url) {
  char *host, *port, *path;

  /* maximum recursion depth */
  if ((++depth) > 10) {
    fatal("Too many redirects");
  }

  /* check if the given URL is valid */
  if (validate_url(url)) {
    fatal("URL must start with 'http://'");
  }
  
  /* extract host, path and port number */
  split_url(url, &host, &port, &path);

  /* download HTML */
  return download_file(host, port, path);
}
