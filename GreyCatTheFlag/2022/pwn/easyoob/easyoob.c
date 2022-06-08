#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BANNER "LeaderboardDB v0.1 alpha"

void ezflag()
{
    system("cat ./flag.txt");
}

typedef struct command
{
    int op;
    int pos;
    int userid;
    int score;
} command;

typedef struct entry
{
    int userid;
    int score;
} entry;

void usage()
{
    puts("This repl currently supports 2 operations.");
    puts("------------------------------");
    puts("1. Read leaderboard entry");
    puts(" > 1 <position>");
    puts("");
    puts("2. New leaderboard entry");
    puts(" > 2 <position> <user id> <score>");
    puts("");
    puts("3. Exit");
    puts(" > 3");
    puts("------------------------------");
}

command get_command()
{
    printf("\n> ");
    command res;
    scanf("%d", &res.op);

    if (res.op != 1 && res.op != 2) return res;

    scanf("%d", &res.pos);

    if (res.op != 2) return res;

    scanf("%d %d", &res.userid, &res.score);
    return res;
}

void handle_read(entry* leaderboard, command cmd)
{
    // printf("|| Reading leaderboard at position %d\n", cmd.pos);
    printf("%d. [%d]  %d\n", cmd.pos, leaderboard[cmd.pos].userid, leaderboard[cmd.pos].score);
}

void handle_write(entry* leaderboard, command cmd)
{
    leaderboard[cmd.pos].userid = cmd.userid;
    leaderboard[cmd.pos].score = cmd.score;
    printf("%d. [%d]  %d\n", cmd.pos, leaderboard[cmd.pos].userid, leaderboard[cmd.pos].score);
}

void setup_io()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main()
{
    entry leaderboard[20];

    setup_io();
    puts(BANNER);
    usage();

    command cmd;
    do {
        cmd = get_command();
        if (cmd.op == 1) handle_read(leaderboard, cmd);
        else if (cmd.op == 2) handle_write(leaderboard, cmd);
    } while (cmd.op != 3);

    puts("Thanks for using LeaderboardDB. Your changes are not saved.");

    return 0;
}