#include <stdio.h>
#include <stdlib.h>

void main()
{
    int var;
    long int check = 0x04030201;
    char buf[0x30];

    puts("Hello kind sir!");
    printf("My variable \"check\" value is %p.\nCould you change it to 0xc0febabe?\n", check);
    printf("This is the current buffer: %s\n", buf);
    fgets(buf, 0x40, stdin);

    if (check == 0x04030201)
    {
        puts("Mmmh not quite...\n");
    }
    if (check != 0x04030201 && check != 0xc0febabe)
    {
        puts("Mmmh getting closer!...");
        printf("This is the new value of \"check\": %p\n", check);
    }
    if (check == 0xc0febabe)
    {
        puts("Thanks man, you're a life saver!\nHere is your reward, a shell! ");
        system("/bin/sh");
        puts("Bye bye!\n");
    }
}