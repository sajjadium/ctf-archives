#include <stdio.h>
#include <string.h>

const char *available_toppings[] = {"pepperoni",  "cheese",     "olives",
                                    "pineapple",  "apple",      "banana",
                                    "grapefruit", "kubernetes", "pesto",
                                    "salmon",     "chopsticks", "golf balls"};
const int num_available_toppings =
    sizeof(available_toppings) / sizeof(available_toppings[0]);

int main(void) {
  setbuf(stdout, NULL);
  printf("Welcome to kaiphait's pizza shop!\n");
  while (1) {
    printf("Which toppings would you like on your pizza?\n");
    for (int i = 0; i < num_available_toppings; ++i) {
      printf("%d. %s\n", i, available_toppings[i]);
    }
    printf("%d. custom\n", num_available_toppings);
    char toppings[3][100];
    for (int i = 0; i < 3; ++i) {
      printf("> ");
      int choice;
      scanf("%d", &choice);
      if (choice < 0 || choice > num_available_toppings) {
        printf("Invalid topping");
        return 1;
      }
      if (choice == num_available_toppings) {
        printf("Enter custom topping: ");
        scanf(" %99[^\n]", toppings[i]);
      } else {
        strcpy(toppings[i], available_toppings[choice]);
      }
    }
    printf("Here are the toppings that you chose:\n");
    for (int i = 0; i < 3; ++i) {
      printf(toppings[i]);
      printf("\n");
    }
    printf("Your pizza will be ready soon.\n");
    printf("Order another pizza? (y/n): ");
    char c;
    scanf(" %c", &c);
    if (c != 'y') {
      break;
    }
  }
}
