#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include "rules.h"

typedef struct Translator {
  void (*translate)(char*);
  char *text;
  int size;
} Translator;

void english_expand(char *text) {
  int i, alen, blen;
  Rule *r;
  char *p, *q;
  char *end = &text[strlen(text)-1]; // pointer to the last character

  /* Replace all abbreviations */
  for (p = text; *p; ++p) {
    for (i = 0; i < sizeof(rules) / sizeof(Rule); i++) {
      r = &rules[i];
      alen = strlen(r->a);
      blen = strlen(r->b);
      if (strncasecmp(p, r->a, alen) == 0) {
        // i.e "i'm pwn noob." --> "i'm pwn XXnoob."
        for (q = end; q > p; --q)
          *(q+blen-alen) = *q;
        // Update end
        end += blen-alen;
        *(end+1) = '\0';
        // i.e "i'm pwn XXnoob." --> "i'm pwn newbie."
        memcpy(p, r->b, blen);
      }
    }
  }
}

Translator *translator_new(int size) {
  Translator *t;

  /* Allocate region for text */
  char *text = (char*)calloc(sizeof(char), size);
  if (text == NULL)
    return NULL;

  /* Initialize translator */
  t = (Translator*)malloc(sizeof(Translator));
  t->text = text;
  t->size = size;
  t->translate = english_expand;

  return t;
}

void translator_reset(Translator *t) {
  memset(t->text, 0, t->size);
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(60);

  Translator *t = translator_new(0x1000);
  while (1) {
    /* Input data */
    translator_reset(t);
    printf("Enter text: ");
    fgets(t->text, t->size, stdin);
    if (t->text[0] == '\n')
      break;

    /* Expand abbreviation */
    t->translate(t->text);
    printf("Result: %s", t->text);
  }

  return 0;
}
