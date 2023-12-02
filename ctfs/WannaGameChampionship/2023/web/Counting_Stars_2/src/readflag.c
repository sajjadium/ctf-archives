#include <stdio.h>

int main()
{
    setreuid(geteuid(), getuid());
    system("/usr/bin/cat /flag");
    return 0;
}