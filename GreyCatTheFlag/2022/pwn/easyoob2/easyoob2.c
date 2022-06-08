#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BANNER "LeaderboardDB v0.2 alpha"

typedef struct command
{
    int op;
    int pos;
    char name[4];
    int score;
} command;

typedef struct entry
{
    int score;
    char name[4];
} entry;

void usage()
{
    puts("This repl currently supports 3 operations.");
    puts("------------------------------");
    puts("1. Read leaderboard entry");
    puts(" > 1 <position>");
    puts("");
    puts("2. New leaderboard entry");
    puts(" > 2 <position> <name> <score>");
    puts(" - name can only be 3 characters long, e.g. AAA");
    puts("");
    puts("3. Upperify player name");
    puts(" > 3 <position>");
    puts("");
    puts("4. Exit");
    puts(" > 4");
    puts("------------------------------");
}

command get_command()
{
    printf("\n> ");
    command res;
    scanf("%d", &res.op);

    if (!(res.op >= 1 && res.op <= 3)) return res;

    scanf("%d", &res.pos);

    if (res.op != 2) return res;

    scanf("%3s %d", res.name, &res.score);
    return res;
}

void handle_read(entry* leaderboard, command cmd)
{
    // printf("|| Reading leaderboard at position %d\n", cmd.pos);
    printf("%d. %-4s  %d\n", cmd.pos, leaderboard[cmd.pos].name, leaderboard[cmd.pos].score);
}

void handle_write(entry* leaderboard, command cmd)
{
    memcpy(leaderboard[cmd.pos].name, cmd.name, 4);
    leaderboard[cmd.pos].score = cmd.score;
    printf("%d. %-4s  %d\n", cmd.pos, leaderboard[cmd.pos].name, leaderboard[cmd.pos].score);
}

void handle_upperify(entry* leaderboard, command cmd)
{
    char* name = leaderboard[cmd.pos].name;
    int len = strlen(name);
    for (size_t i = 0; i < len; ++i) name[i] = toupper(name[i]);
    printf("%d. %-4s  %d\n", cmd.pos, leaderboard[cmd.pos].name, leaderboard[cmd.pos].score);
}

void setup_io()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

entry leaderboard[20];

int main()
{
    setup_io();
    puts(BANNER);
    usage();

    command cmd;
    do {
        cmd = get_command();
        if (cmd.op == 1) handle_read(leaderboard, cmd);
        else if (cmd.op == 2) handle_write(leaderboard, cmd);
        else if (cmd.op == 3) handle_upperify(leaderboard, cmd);
    } while (cmd.op != 4);

    puts("Thanks for using LeaderboardDB. Your changes are not saved.");

    return 0;
}