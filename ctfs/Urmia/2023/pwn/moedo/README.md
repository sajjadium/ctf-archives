We've created a moe alternative to sudo called moedo.

If you can bypass its moe secuirty you'll be awarded with the flag!

    telnet moe.uctf.ir 7002
    Username: mashiro
    Password: Qh3VRn@23jv43Q

moedo source code:

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <grp.h>

#define MOE_ENOUGH 0x30e

int check_moe(int uid)
{
    struct group *moe_group = getgrnam("moe");
    int moeness = 0;

    int ngroups;
    gid_t *groups;

    if (moe_group == NULL)
        return 0;

    ngroups = getgroups(0, NULL);
    groups = malloc(ngroups * sizeof(*groups));
    getgroups(ngroups, groups);
    for (int i = 0; i < ngroups; i++)
    {
        if (groups[i] == moe_group->gr_gid)
        {
            moeness = MOE_ENOUGH;
            break;
        }
    }

    free(groups);
    return moeness;
}

int main(int argc, char *argv[])
{
    uid_t uid = getuid();
    uid_t gid = getgid();
    int moeness = check_moe(uid);

    char *custom_chant = getenv("MOE_CHANT");
    char chant[] = "Moe Moe Kyun!";

    if (argc < 2)
    {
        fputs("Missing command\n", stderr);
        return 1;
    }

    if (custom_chant)
        strcpy(chant, custom_chant);

    printf("UID: %u - GID: %u - Moe: %x\n", uid, gid, moeness);

    if (moeness != MOE_ENOUGH)
    {
        fputs("You're not moe enough!\n", stderr);
        return 1;
    }

    if (setuid(0) != 0)
    {
        perror("setuid() failed");
        return 1;
    }
    if (setgid(0) != 0)
    {
        perror("setgid() failed");
        return 1;
    }

    puts(chant);

    if (execvp(argv[1], &argv[1]) != 0)
    {
        perror("execv() failed");
        return 1;
    }

    return 0;
}
