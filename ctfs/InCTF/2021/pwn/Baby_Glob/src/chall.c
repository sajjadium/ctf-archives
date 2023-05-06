/* Header files required for linking gnu-lib */

#include <config.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <glob.h>
#include <errno.h>
#include <stdint.h>
#include <errno.h>

#include "signature.h"
SIGNATURE_CHECK (glob, int, (char const *, int, int (*) (char const *, int),
                             glob_t *));
SIGNATURE_CHECK (globfree, void, (glob_t *));

#include "macros.h"

#define BASE "test-glob.t"
#define GL_NO_SUCH_FILE "/gnulib-magic-does-not-exist"

/* bss table to store path pointers */

char* paths[10] = {0};
unsigned int path_count = 0;

void err(const char *msg){
    perror(msg);
    exit(EXIT_FAILURE);
}

void initialize(){
    setvbuf(stdin,0,_IONBF,0);
    setvbuf(stdout,0,_IONBF,0);
    setvbuf(stderr,0,_IONBF,0);
    return;
}

void getInp(char *buf, unsigned int len){
   int ret = read(0,buf,len) ;
   if(ret<=0){
       err("Read error");
   }
   buf[ret-1]='\0';
   return;
}

unsigned int getInt(){
    char buf[5];
    getInp(buf,5);
    return atoi(buf);
}

unsigned int menu(){
    puts(" ------------------------------------ ");
    puts("| 1. Add Path                        |");
    puts("| 2. Check Path                      |");
    puts("| 3. View Path                       |");
    puts("| 4. Remove Path                     |");
    puts("| 5. Exit                            |");
    puts(" -------------------------------------");
    printf("Choice >> ");
    return getInt();
}

void add_path(){
    printf("[*] Enter idx >> ");
    size_t idx = getInt();
    if(idx < 0 || idx > 10)
        err("[-] Invalid idx");
    else{
        printf("[*] Enter size >> ");
        size_t size = getInt();
        if(size < 0 || size > 0x1000)
            err("[-] Too big");
        char *pattern = (char *)malloc(size);
        printf("[*] Enter path >> ");
        getInp(pattern,size);
        if(path_count>10)
            err("[-] Max Paths storage limit");
        else{
            if(!paths[idx]){
                paths[idx] = pattern;
                path_count++;
                puts("[+] Path added");
            }
            else{
                err("[-] Path exists");
            }
        }
    }
}


/* The glob() function finds pathnames matching the given pattern. */
void check_path(){
    printf("[*] Enter idx >> ");
    size_t idx = getInt();
    if(!paths[idx])
        err("[-] Path entry doesnt exist");

	glob_t pglob = { .gl_pathc = 0 };

    if (glob((char *) paths[idx], GLOB_MARK|GLOB_TILDE, NULL, &pglob) == 0){
        puts("[+] Path found");
        printf("%s\n",pglob.gl_pathv[0]);
    }
    else
        puts("[-] Path not found");
}

void view_path(){
    printf("[*] Enter idx >> ");
    size_t idx = getInt();
    if(!paths[idx])
        err("[-] Path entry doesnt exist");
    printf("[+] Path : ");
    write(1,paths[idx],sizeof(paths[idx]));
    printf("\n");
}

void remove_path(){
    printf("[*] Enter idx >> ");
    size_t idx = getInt();
    if(!paths[idx])
        err("[-] Path entry doesnt exist");
    free(paths[idx]);
    paths[idx] = NULL;
    puts("[+] Path removed");
}

int main(int argc, char **argv)
{
    initialize();
    while(1){
        size_t choice = menu();
        switch(choice){
            case 1: 
                add_path(); 
                break;
            case 2: 
                check_path(); 
                break;
            case 3:
                view_path();
                break;
            case 4:
                remove_path();
                break;
            case 5:
                err("[-] Exit");
            default:
                puts("[-] Invalid choice");
        }
    }
}
