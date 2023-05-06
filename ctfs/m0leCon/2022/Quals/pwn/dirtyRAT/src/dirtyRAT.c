#define _GNU_SOURCE
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>

#define CONFIG_PATH "./conf"
#define CONFIG_HEADER "##DIRTY CONFIG HEADER\n"
#define MAX_FILENAME_LEN 7
#define MAX_FILEDATA_LEN 257

// globals r gud programming practice bc im lazy
int p[2];

int checkRestricted(char *target){
    char buf[MAX_FILENAME_LEN];
    char header[64];
    int len = strlen(target);
    FILE *f = fopen(CONFIG_PATH, "r");

    for(int i = 0; i<len; i++){
        if(target[i] == '/' || target[i] == '\\' || target[i] == '.' || target[i] == '~'){
            printf("Sneaky stuff not allowed! >:-(\n");
            return 0;
        } else if(target[i] == '\n')
            target[i] = 0;
    }

    fgets(header, sizeof(CONFIG_HEADER), f);
    if(strcmp(header, CONFIG_HEADER)){
    printf("CONFIG HEADER CORRUPTED. BYE!\n");
    exit(-1);
    }

    while(fgets(buf, MAX_FILENAME_LEN, f)) {
        int l = strlen(buf);
        if(buf[l-1] == '\n')
            buf[l-1] = 0;

        if(!strcmp(target, buf)){
            fclose(f);
            return 1;
        }
    }

    fclose(f);
    printf("You should have paid me more for that file ehehheheheheheheh\n");
    return 0;
}

void childWrite(char *fname, unsigned int len){
    FILE *f = fopen(fname, "w");
    int i = 0;
    char c;

    if (f == NULL) {
        printf("Failed to open file! Maybe read only? Eheheheheheheh\n");
        while(i < len){
            read(p[0], &c, 1);
            i++;
        }
        exit(1);
    }

    while(i < len){
        read(p[0], &c, 1);
        fputc(c, f);
        i++;
    }
    exit(0);
}

void childRead(char *fname, u_int8_t len){
    int f = open(fname, O_RDONLY);
    int i = 0;
    char c = 0;

    if (f < 0) {
        printf("Failed to open file??\n");
        exit(1);
    }

    loff_t offset = 0;
    int nbytes = splice(f, &offset, p[1], NULL, len, 0);
    sleep(2);
    if (nbytes <= 0) {
        printf("Something failed during read :(\n");
        exit(1);
    }

    exit(0);
}

void writeFile(){
    char fname[MAX_FILENAME_LEN];

    printf("Insert filename: ");
    scanf("%5s", fname);
    while(getchar() != '\n');

    if(checkRestricted(fname)){
        int dataLen, padLen, i = 0;
        unsigned int maxPad = fcntl(p[1], F_GETPIPE_SZ);
        char data[MAX_FILEDATA_LEN];

        printf("Write data (ASCII, non space and max %d, upgrade plan for more features): ", MAX_FILEDATA_LEN-1);
        scanf("%256s", data);
        while(getchar() != '\n');

        dataLen = strlen(data);
        printf("Read %d bytes\n", dataLen);
        if(dataLen > MAX_FILEDATA_LEN-1)
            dataLen = MAX_FILEDATA_LEN-1;

        // zero-padding is 4 k00l kidz\x00\x00\x00\x00\x00
        printf("How many padding bytes? (0-%d): ", maxPad-dataLen);
        scanf("%d", &padLen);
        while(getchar() != '\n');

        if(padLen > maxPad-dataLen)
            padLen = maxPad-dataLen;

        if(padLen < 0)
            padLen = 0;

        write(p[1], data, dataLen);
        char c = 0;
        i = 0;

        while(i < padLen){
            write(p[1], &c, 1);
            i++;
        }

        // spawning a child to do the dirty job
        int cpid = fork();
        int cstatus = 0;
        if(cpid){
            // parent
            waitpid(cpid, &cstatus, 0);
        }else{
            // child
            childWrite(fname, dataLen+padLen);
        }

        if(!WEXITSTATUS(cstatus))
            printf("File written!\n");
    }
}

void readFile(){
    char fname[MAX_FILENAME_LEN];

    printf("Insert filename: ");
    scanf("%5s", fname);
    while(getchar() != '\n');

    if(checkRestricted(fname)){
        char data[MAX_FILEDATA_LEN];
        int8_t dataLen = 0;

        printf("How many bytes to read? (Max 127 eheheeheh): ");
        scanf("%hhd", &dataLen);
        while(getchar() != '\n');

        // spawning a child to do the dirty job
        int cpid = fork();
        if(cpid){
            // parent
            int cstatus = 0;
            waitpid(cpid, &cstatus, 0);

            if(!WEXITSTATUS(cstatus)){
                if (dataLen < 0)
                    dataLen = 0;

                read(p[0], data, dataLen);
                data[dataLen] = 0;
                printf("File content:\n");
                printf("%s\n", data);
                printf("File read!\n");
            }
        }else{
            // child
            childRead(fname, dataLen);
        }
    }
}

void list(){
    system("ls -al .");
    return;
}

void banner(){
    setbuf(stdout, NULL);
    printf("Welcome to\n");
    printf("                                                                                               \n");
    printf("         88  88                                    88888888ba          db    888888888888  \n");
    printf("         88  \"\"                ,d                  88      \"8b        d88b        88       \n");
    printf("         88                    88                  88      ,8P       d8'`8b       88       \n");
    printf(" ,adPPYb,88  88  8b,dPPYba,  MM88MMM  8b       d8  88aaaaaa8P'      d8'  `8b      88       \n");
    printf("a8\"    `Y88  88  88P'   \"Y8    88     `8b     d8'  88\"\"\"\"88'       d8YaaaaY8b     88       \n");
    printf("8b       88  88  88            88      `8b   d8'   88    `8b      d8\"\"\"\"\"\"\"\"8b    88       \n");
    printf("\"8a,   ,d88  88  88            88,      `8b,d8'    88     `8b    d8'        `8b   88       \n");
    printf(" `\"8bbdP\"Y8  88  88            \"Y888      Y88'     88      `8b  d8'          `8b  88       \n");
    printf("                                          d8'                                              \n");
    printf("                                         d8'                                               CLI\n");
    printf("Victim info:\t");
    system("uname -a");
    printf("Whoami:\t\t");
    system("whoami");
    pipe(p);
}

void menu(){
    printf("\nAvailable commands:\n");
    printf("1)List files in folder.\n");
    printf("2)Read file from our curated list of important files :)\n");
    printf("3)Write data to one file from our curated list of important files :)\n");
    printf("4)Win the CTF for me pls ≧◡≦\n");
    printf("-1)Quit\n");
}

int main(void){
    int choice;
    char loop = 1;

    banner();

    while(loop){
        menu();
        printf("\nYour choice: ");
        scanf("%d", &choice);
        while(getchar() != '\n');

        switch(choice){
            case 1:
                list();
                break;
            case 2:
                readFile();
                break;
            case 3:
                writeFile();
                break;
            case 4:
                puts("Sure, 9999999999 points addedd to your score, ur welcome!\n");
                break;
            case -1:
                loop = 0;
                break;
            default:
                printf("Unrecognized command.\n");
        }
    }
}
