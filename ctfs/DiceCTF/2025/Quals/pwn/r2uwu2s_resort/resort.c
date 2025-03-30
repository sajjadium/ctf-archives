#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>

#define ANSI_RESET "\x1b[0m"
#define ANSI_COLOR(x) "\x1b[0;" x "m"
#define ANSI_RED ANSI_COLOR("31")
#define ANSI_GREEN ANSI_COLOR("32")
#define ANSI_YELLOW ANSI_COLOR("33")
#define ANSI_BLUE ANSI_COLOR("34")
#define ANSI_MAGENTA ANSI_COLOR("35")
#define ANSI_CYAN ANSI_COLOR("36")
#define ANSI_WHITE ANSI_COLOR("37")
#define ANSI_BRIGHT_RED ANSI_COLOR("91")
#define ANSI_BRIGHT_GREEN ANSI_COLOR("92")
#define ANSI_BRIGHT_YELLOW ANSI_COLOR("93")
#define ANSI_BRIGHT_BLUE ANSI_COLOR("94")
#define ANSI_BRIGHT_MAGENTA ANSI_COLOR("95")
#define ANSI_BRIGHT_CYAN ANSI_COLOR("96")
#define ANSI_BRIGHT_WHITE ANSI_COLOR("97")
#define ANSI_ERASE "\x1b[2J"

#define sleep_ms(x) usleep(x * 1000)

typedef struct {
  int8_t hp;
} dustbunny;

void print_bunny(dustbunny* bunny, char paw) {
  if (bunny->hp > 50) {
    printf("%1$c{ ^^ }%1$c", paw);
  } else if (bunny->hp > 0) {
    printf("%1$c{ oo }%1$c", paw);
  } else {
    printf("%1$c{ xx }%1$c", paw);
  }
}

void print_ui(char* msg, dustbunny bunnies[static 3], uint8_t hp, uint8_t mp) {
  printf(
    ANSI_BRIGHT_RED \
    "                                        \n" \
    "  +==================================+  \n" \
    "  |                                  |  \n" \
    "  | "
  );
  printf("%-32s", msg);
  printf(
    " |  \n" \
    "  |                                  |  \n" \
    "  |     "
  );
  print_bunny(&bunnies[0], '*');
  print_bunny(&bunnies[1], '\'');
  print_bunny(&bunnies[2], '.');
  printf(
    "     |  \n" \
    "  |                                  |  \n" \
    "  +==================================+  \n" \
    "  |                                  |  \n" \
    "  | r2uwu2 @ "
  );
  printf("%-23p", &print_ui);
  printf(
    " |  \n" \
    "  | ------ HP ["
  );
  for (uint8_t i = 0; i < 20; i++) {
    printf(i < hp / 5 ? "#" : " ");
  }
  printf(
    "] |  \n" \
    "  |        MP ["
  );
  for (uint8_t i = 0; i < 20; i++) {
    printf(i < mp / 5 ? "*" : " ");
  }
  printf(
    "] |  \n" \
    "  |                                  |  \n" \
    "  +==================================+  \n" \
    "                                        \n" \
    ANSI_RESET
  );
}

char* items[] = {
  "random bs",
  "spooky rizz",
  "dr chatterjee",
  "DOM CLOBBERING",
};

int main() {
  dustbunny bunnies[3] = {
    {
      .hp = 96,
    },
    {
      .hp = 99,
    },
    {
      .hp = 97,
    }
  };
  uint8_t hp = 100;
  uint8_t mp = 100;

  char msg[33] = "3 Dust Bunnies block your path! ";
  while (true) {
    print_ui(msg, bunnies, hp, mp);

    int item = rand() % 4;
    int choice;
    printf("Attack with [%s] against which bunny? (1-3) > ", items[item]);
    fflush(stdout);
    if (scanf("%d%*[^\n]", &choice) == 0) {
      puts("bad input >:(");
      fflush(stdout);
      return 1;
    }

    uint8_t dmg;
    if (item == 3) {
      bunnies[choice - 1].hp = 0;
    } else {
      dmg = rand() % 255;
      bunnies[choice - 1].hp -= dmg;
    }

    hp -= 1;
    if (bunnies[choice - 1].hp <= 0) {
      sprintf(msg, "Bunny %d has fallen!", choice);
    } else {
      sprintf(msg, "Bunny %d took %d damage!", choice, dmg);
    }

    if (bunnies[0].hp <= 0 && bunnies[1].hp <= 0 && bunnies[2].hp <= 0) {
      puts("r2uwu2 wins!");
      fflush(stdout);
      return 0;
    } else if (hp < 0) {
      puts("the resort wins...");
      fflush(stdout);
      return 1;
    }
  }
}
