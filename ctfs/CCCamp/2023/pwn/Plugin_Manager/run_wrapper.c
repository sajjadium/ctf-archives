#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
    setuid( 0 );   // you can set it at run time also
    chdir("/opt/pluginmanager/bin/");
    char *env[] = {"PATH=/opt/pluginmanager/bin/", NULL};
    execle( "/usr/bin/mono", "/usr/bin/mono", "/opt/pluginmanager/bin/CatRunner.exe", NULL, env);
    return 0;
 }