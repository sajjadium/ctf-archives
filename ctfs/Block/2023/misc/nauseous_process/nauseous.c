#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include "getflag.h"

typedef char *get_flag_fct_type();

struct arbitrary_struct {
    char barf_buf[64];
    void *get_flag_func;
};

void print_all_cool_like(char *str, int speed)
{
    struct timespec ts;
    ts.tv_nsec = speed;
    ts.tv_sec = 0;
    for (int i = 0; i < strlen(str); i++)
    {
        putchar(i[str]);
        fflush(stdout);
        nanosleep(&ts, 0);
    }
}

void be_annoying()
{
    int fast = 10000000;
    int slow = 700000000;
    struct arbitrary_struct instance;
    instance.get_flag_func = get_flag;
    print_all_cool_like("Hi! welcome to the easiest challenge in this competition! I'm literally just gonna GIVE you the flag!", fast);
    print_all_cool_like("\n\n\n", slow);
    print_all_cool_like("I'm just gonna call up my buddy, getflag.so, to go get that for ya and you can be on your way to the flag submission box...", fast);
    print_all_cool_like("\n\n\n", slow);
    print_all_cool_like("Just gonna", fast);
    print_all_cool_like("... ", slow);
    print_all_cool_like("call", fast);
    print_all_cool_like("... ", slow);
    print_all_cool_like("getflag", fast);
    print_all_cool_like("... ", slow);
    print_all_cool_like("Sorry, I'm just not feeling so good", fast);
    print_all_cool_like("... ", slow);
    print_all_cool_like("In fact, I think i'm gonna", fast);
    print_all_cool_like("... ", slow);
    print_all_cool_like("gonna", fast);
    print_all_cool_like("... ", slow);
    sleep(1);
    char *barf = "BLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARGH";
    print_all_cool_like(barf, fast);
    strcpy(instance.barf_buf, barf);
    print_all_cool_like("\n\n\n\n\n", slow);
    print_all_cool_like("oh god", fast);
    print_all_cool_like("... ", slow);
    print_all_cool_like("WHAT HAVE I DONE", fast);
    print_all_cool_like("... ", slow);
    print_all_cool_like("I BARFED ALL OVER THE GETFLAG POINTER!", fast);
    print_all_cool_like(" ", slow);
    print_all_cool_like("the kernel is gonna KILL me if I dont get this right!", fast);
    print_all_cool_like(" ", slow);
    print_all_cool_like("YOU GOTTA HELP ME!", fast);
    print_all_cool_like("!!", slow);
    print_all_cool_like("\nOKOKOK here's what we do, i'll let you inspect my stack. I don't know how all this linker stuff works, YOU just poke around until you find the get_flag function again and once you do just let me know. deal?", fast);
    print_all_cool_like("\n", slow);
    print_all_cool_like("Just give me an offset from where I barfed and I'll tell you what word is sitting there.", fast);
    print_all_cool_like(" ", slow);
    print_all_cool_like("When you say \"get_flag is at 0x<address>\" I'll just jump on over there, hopefully I don't go", fast);
    print_all_cool_like(" ", slow);
    print_all_cool_like("SPLAT", fast);
    print_all_cool_like(" ", slow);
    print_all_cool_like("on readable memory, you get your flag, I exit(0), everybody wins. alright here goes: ", fast);
    
    char inp[64];
    while (1)
    {
        fgets(inp, sizeof(inp), stdin);
        if (strstr(inp, "get_flag is at 0x"))
        {
            print_all_cool_like("oh you're ready? alright if you say so. the flag is: ", fast);
            long flag_func = strtol(strstr(inp, "0x"), NULL, 0);
            puts(((get_flag_fct_type *)flag_func)());
            exit(0);
        }
        long offset;
        sscanf(inp, " %ld", &offset);
        print_all_cool_like("hmm the value there looks like ", offset);
        for (int i = 0; i < sizeof(size_t); i++)
        {
            printf("%02X ", instance.barf_buf[offset + i] & 0xff);
        }
        puts("");
    }
}

int main()
{
    be_annoying();
}