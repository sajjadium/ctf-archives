#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/*
 * Utilities
 */
ssize_t readline(const char *msg, char **ptr) {
  ssize_t size, n = 0;
  *ptr = NULL;

  /* Input a line of string */
  printf("%s", msg);
  if ((size = getline(ptr, &n, stdin)) <= 0)
    exit(1);

  /* Remove last newline */
  (*ptr)[--size] = '\0';
  if (size <= 0)
    exit(1);

  return size;
}

double readv(const char *msg) {
  double v;

  /* Input a double value */
  printf("%s", msg);
  if (scanf("%lf%*c", &v) <= 0)
    exit(1);

  return v;
}

/*
 * Program
 */
typedef struct _Item {
  char *key;
  double value;
  struct _Item *next;
} Item;

Item *top = NULL;

Item *item_add(char *key, double value) {
  /* Allocate a new item */
  Item *item = (Item*)malloc(sizeof(Item));
  if (!item) return NULL;

  /* Set data to item */
  item->key = key;
  item->value = value;
  item->next = top;

  /* Link to list */
  top = item;
  return item;
}

void item_del(Item *item) {
  if (top == item) {
    /* Removing the first item is special */
    top = item->next;
    free(item->key);
    free(item);
  } else {
    /* Otherwise scan list */
    for (Item *cur = top; cur != NULL; cur = cur->next) {
      if (cur->next == item) {
        /* Unlink item */
        cur->next = item->next;
        free(item->key);
        free(item);
        break;
      }
    }
  }
}

Item *item_lookup(const char *key, size_t keylen) {
  for (Item *cur = top; cur != NULL; cur = cur->next) {
    if (memcmp(key, cur->key, keylen) == 0)
      return cur; /* Found item */
  }
  return NULL; /* Item not found */
}

void item_write_all(FILE *fp) {
  /* Write all items to file */
  fseek(fp, SEEK_SET, 0);
  for (Item *cur = top; cur != NULL; cur = cur->next)
    fprintf(fp, "%s %lf\n", cur->key, cur->value);
  fflush(fp);
}

int main(void) {
  FILE *fp;
  int is_saved;
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);

  if (!(fp = fopen("/dev/null", "w"))) {
    /* We use /dev/null for experimental purpose */
    perror("/dev/null");
    return 1;
  }

  puts("1. add");
  puts("2. get");
  puts("3. del");
  puts("4. save");
  puts("x. exit");
  is_saved = 1;
  while (1) {
    int choice = (int)readv("> ");
    switch (choice)
      {
      case 1: { /* add */
        char *key;
        double value;

        /* Input key-value pair */
        readline("Key: ", &key);
        value = readv("Value: ");

        /* Add item */
        if (item_add(key, value)) {
          is_saved = 0;
          puts("Item added");
        } else {
          puts("Memory error");
          return 1;
        }
        break;
      }

      case 2: { /* get */
        char *key;

        /* Find item by key */
        size_t key_len = readline("Key: ", &key);
        Item *item = item_lookup(key, key_len);

        /* Show value */
        if (item)
          printf("Item: %.02lf\n", item->value);
        else
          puts("Item not found");

        free(key);
        break;
      }

      case 3: { /* del */
        char *key;

        /* Find item by key */
        size_t key_len = readline("Key: ", &key);
        Item *item = item_lookup(key, key_len);

        /* Remove item */
        if (item) {
          item_del(item);
          is_saved = 0;
          puts("Item deleted");
        } else {
          puts("Item not found");
        }

        free(key);
        break;
      }

      case 4: { /* save */
        item_write_all(fp);
        is_saved = 1;
        puts("Items saved");
        break;
      }

      default: { /* exit */
        char ans;
        fclose(fp);

        if (!is_saved) {
          /* Ask when list is not saved */
          puts("The latest item list has not been saved yet.");
          puts("Would you like to discard the changes? [y/N]");
          scanf("%c%*c", &ans);
          if (ans != 'y' && ans != 'Y')
            break;
        }

        puts("Bye (^o^)ﾉｼ");
        return 0;
      }
    }
  }
}
