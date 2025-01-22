#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>

#include "aes.h"

static inline struct timespec difftimespec(struct timespec t1, struct timespec t0)
{
	return (t1.tv_nsec >= t0.tv_nsec)
		? (struct timespec){ t1.tv_sec - t0.tv_sec    , t1.tv_nsec - t0.tv_nsec             }
		: (struct timespec){ t1.tv_sec - t0.tv_sec - 1, t1.tv_nsec - t0.tv_nsec + 1000000000};
}

static inline double timespec_to_nsec(struct timespec t)
{
	return t.tv_sec * 1000000000.0 + t.tv_nsec / 1.0;
}

void menu(){
    printf("1. Encrypt\n2. Decrypt\n3. Exit\n");
}

int getChoice(){
    int result;
    printf("> ");
    fflush(stdout);
    scanf("%d", &result);
    getc(stdin);
    return result;
}

int char2int(char h)
{
    if( isdigit(h) )
        return( h - '0');
    h = toupper(h);
    if( h >= 'A' && h <= 'F' )
        return( h - 'A' + 0x0A);
    /* invalid character */
    {   
        printf("\nInvalid hex character: %d\n",h);
        exit(1);
    }   

    return(0);
}

char hex2char(char *hex)
{
    int a,b;

    a = char2int(*(hex+0)); /* first character */
    b = char2int(*(hex+1)); /* second char */

    return( (a << 4) + b);
}

int getHex(char *buf){
    for (size_t i = 0; i < 16; i++)
    {
        char hex[3];
        hex[0] = getc(stdin);
        hex[1] = getc(stdin);
        hex[2] = '\0';
        buf[i] = hex2char(hex);
    }
    getc(stdin);
}

void printHex(char *buf, int len){
    for (int i = 0; i < len; i++)
    {
        printf("%02hhX", buf[i]);
    }
}

void encrypt(u_int8_t *key){
    char msg[16];
    char enc[16];
    printf("Input the message to encrypt (in hex): ");
    fflush(stdout);
    getHex(msg);

    struct timespec initial;
	struct timespec end;
	clock_gettime(CLOCK_MONOTONIC, &initial);
    aesBlockEncrypt(key, msg, enc);
    clock_gettime(CLOCK_MONOTONIC, &end);

    printf("Result: ");
    printHex(enc, 16);

    printf("\nEncryption took %f ns\n", timespec_to_nsec(difftimespec(end, initial)));
}

void decrypt(u_int8_t *key){
    char msg[16];
    char enc[16];
    printf("Input the message to decrypt (in hex): ");
    fflush(stdout);
    getHex(enc);

    struct timespec initial;
	struct timespec end;
	clock_gettime(CLOCK_MONOTONIC, &initial);
    aesBlockDecrypt(key, enc, msg);
    clock_gettime(CLOCK_MONOTONIC, &end);

    printf("Result: ");
    printHex(msg, 16);

    printf("\nDecryption took %.2f ns\n", timespec_to_nsec(difftimespec(end, initial)));
}

int main(){
    menu();
    u_int8_t key[16];
    int keyfd = open("flag.txt", O_RDONLY);
    if (keyfd == -1){
        perror("Error getting random: ");
        exit(1);
    }

    int err = read(keyfd, key, 16);
    if (err == -1){
        perror("Error getting random: ");
        exit(1);
    }

    close(keyfd);

    while (1)
    {
        int choice = getChoice();
        switch (choice)
        {
        case 1:
            encrypt(key);
            break;
        case 2:
            decrypt(key);
            break;
        case 3:
            exit(0);
            break;
        default:
            printf("That is not an option");
            break;
        }
    }
}