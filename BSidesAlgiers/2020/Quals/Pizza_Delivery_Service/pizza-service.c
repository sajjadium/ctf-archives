#include "pizza-service.h"

void setup(void) {
    setvbuf(stdin, NULL, 2, 0);
    setvbuf(stdout, NULL, 2, 0);
    setvbuf(stderr, NULL, 2, 0);
}

void banner(void) {
  printf("\
 _____ _                _____       _ _                         _____                 _          \n\
|  __ (_)              |  __ \\     | (_)                       / ____|               (_)         \n\
| |__) | __________ _  | |  | | ___| |___   _____ _ __ _   _  | (___   ___ _ ____   ___  ___ ___ \n\
|  ___/ |_  /_  / _` | | |  | |/ _ \\ | \\ \\ / / _ \\ '__| | | |  \\___ \\ / _ \\ '__\\ \\ / / |/ __/ _ \\\n\
| |   | |/ / / / (_| | | |__| |  __/ | |\\ V /  __/ |  | |_| |  ____) |  __/ |   \\ V /| | (_|  __/\n\
|_|   |_/___/___\\__,_| |_____/ \\___|_|_| \\_/ \\___|_|   \\__, | |_____/ \\___|_|    \\_/ |_|\\___\\___|\n\
                                                        __/ |                                    \n\
                                                       |___/                                     \n");
}

int menu(void) {
  printf(
    "1- Add new order\n"
    "2- Edit order\n"
    "3- View order\n"
    "4- Deliver order\n"
    "5- Relogin\n"
    "6- Exit\n\n"
  );

  return read_num("Choose an option : ");
}

void read_line(char *msg, char *buf, unsigned int max_size) {
  int i, c;

  printf("%s", msg);
  for (i = 0; i < max_size-1; i++) {
    c = getchar();
    if (c == EOF || (char)c == '\n') {
      break;
    }
    buf[i] = (char)c;
  }
  buf[i] = '\0';
}

int read_num(char *msg) {
  char buf[12];

  read_line(msg, buf, 12);
  return atoi(buf);
}

void take_order(struct order *order) {
  int choice = -1, with_soda;
  char buf[4];
  float total_price;

  for (int i = 0; i < NUM_TYPES; i++) {
    printf("%d- %s Pizza ($%.2f)\n", i+1, pizza_types[i], pizza_prices[i]);
  }

  putchar('\n');
  while (!(choice >= 1 && choice <= NUM_TYPES)) {
    choice = read_num("No. of pizza type : ");
  }

  printf("With soda ($%.2f) ?[y/n] ", soda_price);
  read_line("", buf, 4);
  with_soda = (buf[0] == 'y');

  total_price = pizza_prices[choice-1] + ((with_soda) ? soda_price : 0);

  read_line("Address where to deliver the order : ", order->address, ADDR_SIZE);
  order->pizza_type = pizza_types[choice-1];
  order->with_soda = with_soda;
  order->total_price = total_price;
}

int read_idx(void) {
  int idx;

  idx = read_num("Order no. : ") - 1;
  if (!(idx >= 0 && idx < MAX_ORDERS)) {
    fprintf(stderr, "Order doesn't exist !\n");
    return -1;
  }

  return idx;
}

void add(void) {
  int idx;
  struct order *order;

  for (idx = 0;
      idx < MAX_ORDERS && orders[idx] != NULL;
      idx++);
  if (idx == MAX_ORDERS) {
    fprintf(stderr, "Max number of orders reached !\n");
    return;
  }

  orders[idx] = (struct order*)malloc(sizeof(struct order));
  if (orders[idx] == NULL) {
    fprintf(stderr, "Internal service error !\n");
    return;
  }
  take_order(orders[idx]);

  printf("Order no. %d taken, that will be $%.2f\n", idx+1, orders[idx]->total_price);

  is_used[idx] = 1;
}

void edit(int idx) {
  view(idx);
  putchar('\n');
  take_order(orders[idx]);

  putchar('\n');
  printf("Order no. %d updated, that will be $%.2f\n", idx+1, orders[idx]->total_price);
}

void view(int idx) {
  putchar('\n');
  printf(
    "---------------------------------------------\n"
    "Order no. : %d\n"
    "Pizza type : %s Pizza\n"
    "With soda : %s\n"
    "Total price : $%.2f\n"
    "Delivery address : %s\n"
    "---------------------------------------------\n",
    idx+1,
    orders[idx]->pizza_type,
    (orders[idx]->with_soda) ? "yes" : "no",
    orders[idx]->total_price,
    orders[idx]->address
  );
}

void deliver(int idx) {
  if (is_used[idx]) {
    free(orders[idx]);
    is_used[idx] = 0;

    putchar('\n');
    printf("Order no. %d on its way to be delivered !\n", idx+1);
  } else {
    fprintf(stderr, "Order doesn't exist !\n");
  }
}

void login(void) {
  char buf[MAX_NAME_SIZE];

  printf("Name (%d characters max) : ", current_user->name_size);
  read_line("", buf, current_user->name_size);

  strncpy(current_user->name, buf, current_user->name_size);
}

int main(int argc, char *argv[]) {
  int choice = -1, idx;

  setup();

  banner();

  current_user = (struct user*)malloc(sizeof(struct user));
  current_user->name_size = MAX_NAME_SIZE;
  current_user->name = (char*)malloc(current_user->name_size);
  login();

  while (choice != 6) {
    putchar('\n');
    printf("Current user : %s\n", current_user->name);
    choice = menu();
    putchar('\n');

    switch(choice) {
      case 1:
	add();
	break;
      case 2:
	idx = read_idx();
	if (idx != -1)
	  edit(idx);
	break;
      case 3:
	idx = read_idx();
	if (idx != -1)
	  view(idx);
	break;
      case 4:
	idx = read_idx();
	if (idx != -1)
	  deliver(idx);
	break;
      case 5:
	login();
    }
  }

  printf("Bye !\n");

  return EXIT_SUCCESS;
}
