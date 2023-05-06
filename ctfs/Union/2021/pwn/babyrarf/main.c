#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

typedef struct attack {
    uint64_t id;
    uint64_t dmg;
} attack;

typedef struct character {
    char name[10];
    int health;
} character;

uint8_t score;

int read_int(){
    char buf[10];
    fgets(buf, 10, stdin);
    return atoi(buf);
}

void get_shell(){
    execve("/bin/sh", NULL, NULL);
}

attack choose_attack(){
    attack a;
    int id;
    puts("Choose an attack:\n");
    puts("1. Knife\n");
    puts("2. A bigger knife\n");
    puts("3. Her Majesty's knife\n");
    puts("4. A cr0wn\n");
    id = read_int();
    if (id == 1){
        a.id = 1;
        a.dmg = 10;
    }
    else if (id == 2){
        a.id = 2;
        a.dmg = 20;
    }
    else if (id == 3){
        a.id = 3;
        a.dmg = 30;
    }
    else if (id == 4){
        if (score == 0){
            puts("l0zers don't get cr0wns\n");
        }
        else{
            a.id = 4;
            a.dmg = 40;
        }
    }
    else{
        puts("Please select a valid attack next time\n");
        a.id = 0;
        a.dmg = 0;
    }
    return a;
}

int main(){
    character player = { .health = 100};
    character boss = { .health = 100, .name = "boss"};
    attack a;
    int dmg;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    srand(0);

    puts("You are fighting the rarf boss!\n");
    puts("What is your name?\n");
    fgets(player.name, 10, stdin);

    score = 10;

    while (score < 100){
        a = choose_attack();
        printf("You choose attack %llu\n", a.id);
        printf("You deal %llu dmg\n", a.dmg);
        boss.health -= a.dmg;
        dmg = rand() % 100;
        printf("The boss deals %llu dmg\n", dmg);
        player.health -= dmg;
        if (player.health > boss.health){
            puts("You won!\n");
            score += 1;
        }
        else{
            puts("You lost!\n");
            score -= 1;
        }
        player.health = 100;
        boss.health = 100;
    }

    puts("Congratulations! You may now declare yourself the winner:\n");
    fgets(player.name, 48, stdin);
    return 0;
}