#include <stdio.h>     // printf
#include <stdlib.h>    // malloc and free
#include <string.h>    // memcpy
#include <sys/stat.h>  //statf


int file_info(char * file)
{
        struct stat statf[1];
        struct stat control[1];

        if (stat(file, statf) < 0)
                return -1;

        /* Turn on stable fields */
        memset(control, 0, sizeof(control));
        control->st_ino = statf->st_ino;
        control->st_dev = statf->st_dev;
        control->st_rdev = statf->st_rdev;
        control->st_uid = statf->st_uid;
        control->st_gid = statf->st_gid;
        control->st_size = statf->st_size;
        control->st_mtime = statf->st_mtime;
        control->st_ctime = statf->st_ctime;

	// Print readable file information
	printf("\nInode Number: %lu\n", control->st_ino);
        printf("Device Number: %lu\n", control->st_dev);
        printf("Device ID: %lu\n", control->st_rdev);
        printf("User ID: %u\n", control->st_uid);
        printf("Group ID: %u\n", control->st_gid);
        printf("File Size: %ld\n", control->st_size);
        printf("Last Modification Time: %ld\n", control->st_mtime);
        printf("Last Status Change Time: %ld\n\n", control->st_ctime);

        return 0;
}


int main(int argc, char ** argv)
{
        file_info(argv[1]);
	return 1;
}


