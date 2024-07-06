#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define NUM_ABILITIES 3
#define NUM_SHEEP 5
#define SHEEP_MAX 20

typedef struct sheep_struct sheep_t;
typedef int (*ability_func)(sheep_t*);
typedef int64_t wool_t;
struct sheep_struct {
    wool_t wps;
    wool_t value;
    unsigned int ability_type;
};
typedef struct {
    int time;
    wool_t wool;
    int num_sheep;
    int free_slot_hint;
    sheep_t* sheep[SHEEP_MAX];
} game_t;
typedef struct {
    wool_t base_wps;
    wool_t buy_value;
    wool_t sell_value;
} sheep_type_t;

int normal(sheep_t*);
int multiply(sheep_t*);
int grow(sheep_t*);
ability_func abilities[NUM_ABILITIES] = {
    normal,
    multiply,
    grow,
};
sheep_type_t sheep_types[NUM_SHEEP] = {
    { .base_wps = 1, .buy_value = 0, .sell_value = 0 },
    { .base_wps = 9, .buy_value = 20, .sell_value = 16 },
    { .base_wps = 25, .buy_value = 50, .sell_value = 40 },
    { .base_wps = 100, .buy_value = 150, .sell_value = 125 },
    { .base_wps = 1000, .buy_value = 500, .sell_value = 450 },
};

void init() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
}

int read_int(char* prompt) {
    int x;
    printf("%s", prompt);
    scanf("%d", &x);
    return x;
}

int menu() {
    puts("1. Buy sheep");
    puts("2. Upgrade sheep");
    puts("3. Sell sheep");
    puts("4. View sheep");
    return read_int("> ");
}

int normal(sheep_t* sheep) {
    return sheep->wps;
};
int multiply(sheep_t* sheep) {
    return 2 * sheep->wps;
};
int grow(sheep_t* sheep) {
    sheep->wps = sheep->wps + 2;
    return sheep->wps;
};

void buy_sheep(game_t* game) {
    if(game->num_sheep >= SHEEP_MAX) {
        puts("Your sheep farm is full!");
        return;
    }

    unsigned int type = read_int("sheep type> ");
    if(type >= NUM_SHEEP) {
        puts("That type of sheep doesn't exist...");
        return;
    }
    if(game->wool < sheep_types[type].buy_value) {
        puts("You can't afford that yet!");
        return;
    }

    sheep_t* sheep = malloc(sizeof(sheep_t));
    sheep->wps = sheep_types[type].base_wps;
    sheep->value = sheep_types[type].sell_value;
    sheep->ability_type = abs(rand()) % 3;

    while(game->sheep[game->free_slot_hint]) game->free_slot_hint++;
    game->sheep[game->free_slot_hint] = sheep;
    game->num_sheep++;
    printf("sheep bought, sitting at index: %d\n", game->free_slot_hint);
}


void upgrade_sheep(game_t* game) {
    int idx = read_int("index> ");
    if(idx >= SHEEP_MAX || game->sheep[idx] == NULL) {
        puts("That sheep doesn't exist!");
        return;
    }

    int upgrade_type = read_int("upgrade type> ");

    if(upgrade_type != 1 || upgrade_type != 2) {
        puts("That upgrade type doesn't exist!");
    }

    if(game->wool <= upgrade_type * 10) {
        puts("You can't afford that yet!");
        return;
    }

    if(upgrade_type == 1) {
        game->sheep[idx]->wps += 1;
    } else if(upgrade_type == 2) {
        game->sheep[idx]->wps *= 2;
    }

    game->sheep[idx]->value += upgrade_type * 9;
    game->wool -= upgrade_type * 10;
}

void sell_sheep(game_t* game) {
    int idx = read_int("index> ");
    if(idx >= SHEEP_MAX || game->sheep[idx] == NULL) {
        puts("That sheep doesn't exist!");
        return;
    }

    game->wool += game->sheep[idx]->value;
    free(game->sheep[idx]);
    game->sheep[idx] = NULL;
    game->free_slot_hint = idx;
    game->num_sheep--;
}

void view_sheep(game_t* game) {
    int idx = read_int("index> ");
    if(idx >= SHEEP_MAX || game->sheep[idx] == NULL) {
        puts("That sheep doesn't exist!");
        return;
    }

    printf("Sheep %d\n", idx);
    printf("\tWPS: %ld\n", game->sheep[idx]->wps);
    printf("\tValue: %ld\n", game->sheep[idx]->value);
}

void update_state(game_t* game) {
    game->time++;
    for(int i = 0; i < game->num_sheep; i++) {
        if(game->sheep[i]) {
            ability_func f = abilities[game->sheep[i]->ability_type];
            game->wool += f(game->sheep[i]);
        }
    }
}

void print_state(game_t* game) {
    printf("Time: %d\n", game->time);
    printf("Wool: %ld\n", game->wool);
    printf("Number of sheep: %d\n", game->num_sheep);
}

int main() {
    init();

    game_t* game = malloc(sizeof(game_t));
    memset(game, 0, sizeof(game_t));

    while(1) {
        int choice = menu();
        switch(choice) {
            case 1:
                buy_sheep(game);
                break;
            case 2:
                upgrade_sheep(game);
                break;
            case 3:
                sell_sheep(game);
                break;
            case 4:
                view_sheep(game);
                break;
            default:
                break;
        }

        update_state(game);
        print_state(game);
    }
}
