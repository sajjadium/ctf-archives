#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void moo(char *msg)
{
        char speak[64];
        int chief_cow = 1;

        strcpy(speak, msg);
        speak[strcspn(speak, "\r\n")] = 0;
        setenv("MSG", speak, chief_cow);

        system("./cowsay $MSG");

}

int main() {
        char buf[1024];
        setbuf(stdout, NULL);
        puts("Welcome to Cowsay as a Service (CaaS)!\n");
        puts("Enter your message: \n");

        fgets(buf, 1024, stdin);
        moo(buf);

        return 0;
}
