#ifndef _HTTPD_H___
#define _HTTPD_H___

#include <stdio.h>
#include <string.h>

// Client request
extern char *method, // "GET" or "POST"
    *uri,            // "/index.html" things before '?'
    *qs,             // "a=1&b=2" things after  '?'
    *prot,           // "HTTP/1.1"
    *payload;        // for POST

extern short payload_size;

// Server control functions
void serve_forever(const char *PORT);

char *request_header(const char *name);

typedef struct {
  char *name, *value;
} header_t;
static header_t reqhdr[30] = {{"\0", "\0"}};
header_t *request_headers(void);

// user shall implement this function

void route();

// Response
#define RESPONSE_PROTOCOL "HTTP/1.1"

// Non authenticated endpoints
#define PUBLIC_RESPONSE_HEADERS printf("Access-Control-Allow-Headers: Authorization\n" \
                                       "Access-Control-Allow-Methods: GET, POST, OPTIONS\n" \
                                       "Access-Control-Allow-Credentials: %s\n" \
                                       "Access-Control-Allow-Origin: %s\n" \
                                       "Content-Type: text/html; charset=UTF-8\n\n", \
                                       request_header("Origin") ? "true" : "false", \
                                       request_header("Origin") ? request_header("Origin") : "*")

// Authenticated API endpoints should not use CORS
#define API_RESPONSE_HEADERS printf("Content-Type: application/json; charset=UTF-8\n\n")
#define API_UNAUTHORIZED_HEADERS printf("WWW-Authenticate: Basic realm=\"Restricted\"\n\n")

#define HTTP_200 printf("%s 200 OK\n", RESPONSE_PROTOCOL)
#define HTTP_401 printf("%s 401 Unauthorized\n", RESPONSE_PROTOCOL)
#define HTTP_404 printf("%s 404 Not found\n", RESPONSE_PROTOCOL)
#define HTTP_500 printf("%s 500 Internal Server Error\n", RESPONSE_PROTOCOL)

// some interesting macro for `route()`
#define ROUTE_START() if (0) {
#define ROUTE(METHOD, URI)                                                     \
  }                                                                            \
  else if (strcmp(URI, uri) == 0 && strcmp(METHOD, method) == 0) {
#define GET(URI) ROUTE("GET", URI)
#define POST(URI) ROUTE("POST", URI)
#define OPTIONS(URI) ROUTE("OPTIONS", URI)
#define ROUTE_END()                                                            \
  }                                                                            \
  else { HTTP_404; PUBLIC_RESPONSE_HEADERS; }

#endif