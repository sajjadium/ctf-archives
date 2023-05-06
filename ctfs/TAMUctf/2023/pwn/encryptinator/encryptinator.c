#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define MAX_LEN 1024
#define FLAG_LEN 30

void upkeep() {
    // Not related to the challenge, just some stuff so the remote works correctly
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void print_hex(char* buf, int len) {
    for (int i=0; i<len; i++) {
        printf("%02x", (unsigned char)buf[i]);
    }
    printf("\n");
}

void encrypt(char* msg, int len, char* iv) {
    char key[len];
    FILE *file;
    
    file = fopen("/dev/urandom", "rb");
    fread(key, len, 1, file);
    fclose(file);    

    for (int i=0; i<len; i++) {
        msg[i] = msg[i] ^ key[i] ^ iv[i % 8];
    }
}

void randomize(char* msg, int len, unsigned long seed, unsigned long iterations) {
    seed = seed * iterations + len;

    if (iterations > 1) {
        randomize(msg, len, seed, iterations- 1);
    } else {
        encrypt(msg, len, ((char *) &seed));
    }
}

char menu() {
    char option;
    printf("\nSelect from the options below:\n");
    printf("1. Encrypt a message\n");
    printf("2. View the encrypted message\n");
    printf("3. Quit\n");
    printf("> ");
    scanf("%c", &option);
    while (getchar() != '\n');
    return option;
}

void console() {
    FILE* file;
    long seed;
    int index;
    int read_len;
    char buf[MAX_LEN] = "";
    int len = -1;

    while (1) {
        switch(menu()) {
            case '1':
                // get user input
                printf("\nPlease enter message to encrypt: ");
                fgets(buf, MAX_LEN-FLAG_LEN, stdin);
                len = strlen(buf);

                // add flag to the buffer
                file = fopen("flag.txt", "rb");
                fread(buf + len, FLAG_LEN, 1, file);
                fclose(file);
                len += FLAG_LEN;

                // encrypt
                seed = ((long) rand()) << 32 + rand();
                randomize(buf, len, seed, buf[0]);
                break;
            case '2':
                if(len == -1) {
                    printf("Sorry, you need to encrypt a message first.\n");
                    break;
                }

                index = 0;
                printf("\nRead a substring of the encrypted message.");
                printf("\nPlease enter the starting index (%d - %d): ", index, len);
                scanf("%d", &index);
                while (getchar() != '\n');

                if (index > len) { 
                    printf("Error, index out of bounds.\n");
                    break;
                }

                printf("Here's your encrypted string with the flag:\n");
                print_hex(buf+index, len - index);
                break;
            case '3':
                printf("goodbye.\n");
                exit(0);
            default:
                printf("There was an error processing that request, please try again.\n");
                break;
        }
    }

}


int main() {
    srand(time(NULL)); 
    upkeep();

    // welcome
    printf("Welcome to my encryption engine: ENCRYPT-INATOR!\n");
    printf("I'll encrypt anything you want but no guarantees you'll be able to decrypt it,\n");
    printf("I haven't quite figured out how to do that yet... :(\n"); 
    console();
}
