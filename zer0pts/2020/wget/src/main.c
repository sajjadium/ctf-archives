#include <stdio.h>
#include <stdlib.h>
#include "oget.h"

/**
 * Entry Point
 */
int main(int argc, char **argv) {
  char *url, *html;

  /* check if URL is given */
  if (argc < 2) {
    printf("Usage: %s <URL>\n", argv[0]);
    return 1;
  } else {
    url = argv[1];
  }

  /* read HTML */
  html = omega_get(url);
  if (html == NULL) {
    fatal("Unknown error");
  } else {
    printf("%s", html);
    free(html);
  }
  return 0;
}
