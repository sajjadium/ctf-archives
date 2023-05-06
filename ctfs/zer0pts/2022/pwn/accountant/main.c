#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

// Credit to Apple Inc.
// https://opensource.apple.com/source/cvs/cvs-44/cvs/lib/allocsa.h.auto.html
#define safe_alloca(N) ((N) < 4032 ? alloca (N) : NULL)

typedef struct {
  int32_t price;
  int32_t quantity;
} Item;

ssize_t get_value(const char *msg) {
  char buf[32];
  printf("%s", msg);
  if (read(0, buf, 31) <= 0) {
    puts("I/O Error");
    exit(1);
  }
  return strtol(buf, NULL, 0);
}

void input_data(Item *items, int i) {
  printf("Item %d:\n", i+1);
  items[i].price = get_value("  Price: $");
  items[i].quantity = get_value("  Quantity: ");
}

void input_all_data(Item *items, int n) {
  for (int i = 0; i < n; i++) {
    input_data(items, i);
  }
}

int64_t calc_total(Item *items, int n) {
  int64_t total = 0;
  int i = n - 1;
  do {
    total += items[i].price * items[i].quantity;
  } while(i-- > 0);
  return total;
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(180);

  Item *items;
  int use_malloc = 0;
  ssize_t n = get_value("Number of items: ");
  if (n <= 0) {
    puts("Invalid value");
    return 1;
  }

  if ((items = safe_alloca(n * sizeof(Item))) == NULL) {
    use_malloc = 1;
    if ((items = calloc(n, sizeof(Item))) == NULL) {
      puts("Memory Error\n");
      return 1;
    }
  }

  input_all_data(items, n);
  printf("Total: $%ld\n", calc_total(items, n));

  if (get_value("Would you like to fix data? [1=Yes] ") == 1) {
    while (1) {
      off_t i = get_value("Index to modify (-1 to quit): ");
      if (i < 0 || i >= n)
        break;
      else
        input_data(items, i);
    }
    printf("Total: $%ld\n", calc_total(items, n));
  }

  puts("Have a nice day at work!");

  if (use_malloc)
    free(items);
}

