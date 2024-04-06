#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <sys/stat.h>
#include <netinet/in.h>
#include <openssl/bio.h>
#include <openssl/evp.h>
#include <openssl/buffer.h>
#include <stdint.h>
#include <dirent.h>
#include <limits.h>

#define MAX_ARGUMENTS 10

struct overall {
    char* work_directory;
    char* minishell;
    char* help;
    char* not_allowed_directory;
    char* not_allowed_file;
    char* file_not_found;
    char* cd_success;
    char cwd[256];
};

struct overall workstation;

void printPrompt() {
    printf("%s", workstation.minishell);
}

void printHelp() {
    printf("%s", workstation.help);
}

void listFiles() {
    DIR *dir;
    struct dirent *entry;

    dir = opendir(".");
    if (dir == NULL) {
        perror("opendir");
        return;
    }
    while ((entry = readdir(dir)) != NULL) {
        if(strcmp(entry->d_name, "..") != 0 && strcmp(entry->d_name, ".") != 0) {
            printf("%s\n", entry->d_name);
        }
        
    }

    closedir(dir);
}

void changeDirectory(char *directory) {
    char cwd[1024];
    char firstDirectory[256];
    if (getcwd(cwd, sizeof(cwd)) == NULL) {
        perror("getcwd");
        return NULL;
    }

    char *next_dir = strchr(directory, '/');
    if(next_dir != NULL) {
        size_t length = next_dir - directory;
        
        strncpy(firstDirectory, directory, length);
        firstDirectory[length] = '\0';

    }
    if (strcmp(cwd, workstation.work_directory) == 0) {
        if (strcmp(directory, "..") == 0 || *directory == '/' || strcmp(firstDirectory, "..") == 0) {
            printf("%s", workstation.not_allowed_directory);
            return;
        }
    }
    if (next_dir) {
        *next_dir = '\0';
        next_dir++;
    }
    if (chdir(directory) != 0) {
        perror("chdir");
        return;
        
    }

    if (next_dir && *next_dir != '\0') {
        changeDirectory(next_dir);
    } else {
        printf("%s", workstation.cd_success);
    }
}
int is_regular_file(const char *path)
{
    struct stat path_stat;
    stat(path, &path_stat);
    return S_ISREG(path_stat.st_mode);
}


void downloadFile(char *filename) {
    char* real_filename = malloc(256 * sizeof(char));
    realpath(filename, real_filename);
    char* cwd = malloc(256 * sizeof(char));
    if (getcwd(cwd, sizeof(cwd)) == NULL) {
        perror("getcwd");
        return NULL;
    }
    strncpy(cwd + strlen(cwd), "/", 1);
    strncpy(cwd + strlen(cwd), filename, strlen(filename));
    cwd[strlen(cwd)] = '\0';
    if (strcmp(real_filename,cwd) != 0) {
        printf("%s", workstation.not_allowed_file);
        return;
    }
    if (is_regular_file(filename) != 1) {
        printf("%s", workstation.file_not_found);
        return;
    }
    FILE *file = fopen(filename, "rb");
    if (!file) {
        perror("fopen");
        return;
    }

    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    fseek(file, 0, SEEK_SET);

    char *buffer = malloc(length);
    if (buffer) {
        fread(buffer, 1, length, file);
    }
    fclose(file);

    BIO *bio, *b64;
    BUF_MEM *bufferPtr;

    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new(BIO_s_mem());
    bio = BIO_push(b64, bio);

    BIO_write(bio, buffer, length);
    BIO_flush(bio);
    BIO_get_mem_ptr(bio, &bufferPtr);
    BIO_set_close(bio, BIO_NOCLOSE);
    BIO_free_all(bio);

    printf("%s\n", (*bufferPtr).data);

    free(buffer);
}

int commandAllowed(char *command) {
    while (*command != '\0') {
        if (*command == ';' || *command == '&' || *command == '|' || *command == '<' || *command == '>' || *command == '`' || 
            *command == '$' || *command == '(' || *command == ')' || *command == '{' || *command == '}' || *command == '[' || 
            *command == ']') {
            return 0;
        }
        command++;
    }
    return 1;
}

void main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    if (getcwd(workstation.cwd, sizeof(workstation.cwd)) == NULL) {
        perror("getcwd");
        return NULL;
    }
    //printf("Current working directory: %s\n", workstation.cwd);

    workstation.work_directory = workstation.cwd;
    workstation.minishell = "spaceshell> ";
    workstation.help = "Available commands:\nhelp - Display this help message\nls - List files and directories\ncd <directory> - Change current directory\ndl <file> - Download a file\nexit - Exit the minishell\n";
    workstation.not_allowed_directory = "You are not allowed to access this directory\n";
    workstation.not_allowed_file = "dl command is only allowed for files in the current directory\n";
    workstation.file_not_found = "File not found\n";
    workstation.cd_success = "Directory changed\n";

    
    
    
    char* buffer = malloc(256 * sizeof(char));
    char* cmd = malloc(256 * sizeof(char));
    char  *arg = malloc(32 * sizeof(char));
    int n;
    char *arguments[MAX_ARGUMENTS];
    char *token;
    int numArguments;
    

    while (1) {
        printPrompt();
        bzero(buffer, 256);
        fgets(buffer, 255, stdin);

        strcpy(cmd, buffer);

        if(!commandAllowed(buffer)) {
            printf("One or more not allowed characters in the command\n");
            continue;
        }


        if (buffer[strlen(buffer) - 1] == '\n') {
            buffer[strlen(buffer) - 1] = '\0';
        }

        

        //printf("Command received: %s\n", buffer);
        if(strlen(buffer) == 0){
            continue;
        }

        token = strtok(buffer, " ");
        numArguments = 0;
            while (token != NULL && numArguments < MAX_ARGUMENTS) {
                arguments[numArguments++] = token;
                token = strtok(NULL, " ");
            }
            arguments[numArguments] = NULL;

            if (strcmp(arguments[0], "help") == 0) {
                printHelp();
            } else if (strcmp(arguments[0], "ls") == 0) {
                if (numArguments > 1) {
                    printf("Usage: ls\n");
                } else {
                    listFiles();
                    system("log ls");
                }
            } else if (strcmp(arguments[0], "cd") == 0) {
                if (numArguments < 2) {
                    printf("Usage: cd <directory>\n");
                } else {
                    changeDirectory(arguments[1]);
                    system("log cd");
                }
            } else if (strcmp(arguments[0], "dl") == 0) {
                if (numArguments < 2) {
                    printf("Usage: dl <file>\n");
                } else {
                    downloadFile(arguments[1]);
                    system("log dl");
                }
            } else if (strcmp(arguments[0], "exit") == 0) {
                break;
            
            }else {
               char  *log = malloc(256 * sizeof(char));
                strcpy(log, "./log Error with command:");


                strcpy(arg, cmd);
                strcat(log, arg);
                system(log);

                printf("Unknow command, this event has been reported\n");
            }
    }
}