#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ORDERS 10
#define ADDR_SIZE 32
#define NUM_TYPES 6
#define MAX_NAME_SIZE 16

// struct defintions

struct user {
  int name_size;
  char *name;
};

struct order {
  char address[ADDR_SIZE];
  char *pizza_type;
  int with_soda;
  float total_price;
};

// global variables

struct user *current_user;
struct order *orders[MAX_ORDERS] = {NULL};
char is_used[MAX_ORDERS] = {0};
char *pizza_types[NUM_TYPES] = {"Cheese", "Pepperoni", "BBQ Chicken", "Veggie", "New York-Style", "Pineapple"};
float pizza_prices[NUM_TYPES] = {5.50, 5.50, 8.50, 7.99, 6.99, 14.99};
float soda_price = 1.50;

// function definitions

void setup(void);
void banner(void);
int menu(void);
void read_line(char *msg, char *buf, unsigned int max_size);
int read_num(char *msg);
void take_order(struct order *order); // read order information
int read_idx(void); // read an order index
void add(void); // add a new order
void edit(int idx); // edit an order
void view(int idx); // view an order
void deliver(int idx); // deliver an order
void login(void); // login a new user
