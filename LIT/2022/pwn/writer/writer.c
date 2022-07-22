#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <seccomp.h>
#define ll long long

int *inptr(){
    int *ptr;
    scanf("%lld", &ptr);
    getchar();
    puts("");

    return ptr;
}

void security(){
        scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);

	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
	seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0);

	seccomp_load(ctx);
	seccomp_release(ctx);
}

int main(){
    puts("Welcome to my writer challenge.\n");

    puts("But first, some security.\n");

    security();

    puts("Ok, first you get one read.\n");

    puts("From where?");
    int *ptr = inptr();

    puts("Here is what's there:");
    printf("%d\n", *ptr);
    puts("");

    puts("Ok, now the legendary write.\n");

    puts("To where?");
    ptr = inptr();

    puts("What?");
    scanf("%d", ptr);
    getchar();
    puts("");

    puts("Was this a good challenge?");

    char a[0x80];
    a[read(0, a, 0x80) - 0x1] = '\0';
    puts("");

    puts("You said:");
    puts(a);

    exit(0);    
}
