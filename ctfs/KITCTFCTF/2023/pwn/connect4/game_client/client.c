#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h> 
#include <string.h>
#include <stdbool.h>
#include <stdint.h>

#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

#include <seccomp.h>


typedef unsigned long long u32;
typedef __uint128_t u128;


#define GAME_SERVER_HOST "127.0.0.1"
#define GAME_SERVER_PORT 7777

#define MAX_BUF_SIZE 0x200


u32 g = 30143167;
u32 p = 186047531;


void init() 
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    // alarm(60);
}


int aes_decrypt(unsigned char *ciphertext, int ciphertext_len, unsigned char *key, unsigned char *plaintext) {
    int len;
    int plaintext_len;

    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    EVP_DecryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL);
    EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len);

    plaintext_len = len;
    EVP_DecryptFinal_ex(ctx, plaintext + len, &len);
    plaintext_len += len;

    EVP_CIPHER_CTX_free(ctx);

    return plaintext_len;
}

int aes_encrypt(unsigned char *plaintext, unsigned char *key, unsigned char *ciphertext) {
    int len;
    int ciphertext_len;
    
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, NULL);
    EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, strlen(plaintext));

    ciphertext_len = len;
    EVP_EncryptFinal_ex(ctx, ciphertext + len, &len);
    ciphertext_len += len;

    EVP_CIPHER_CTX_free(ctx);

    return ciphertext_len;
}

char *readuntil(int fd, char *buf, char delim) {
    int i = 0;
    
    while (read(fd, buf + i, 1) == 1) {
        if (buf[i] == delim) {
            // buf[i] = '\0';
            return buf;
        }
        i += 1;
    }

    return buf;
}

void printreaduntil(int fd, char token) {
    char buf[MAX_BUF_SIZE] = { 0 };

    readuntil(fd, buf, token);
    printf("%s", buf);
}

void printreadline(int fd) {
    printreaduntil(fd, '\n');
}

void writeline(int fd, char *buf, int count) {
    for (int i = 0; i < count; i++) {
        write(fd, buf + i, 1);
    }
    write(fd, "\n", 1);
}


void play_game(int fd) {
    // TODO: this will be in the day 1 patch surely...
}

void init_syscall_filter() {
    // only allow: read, write, exit, exit_group, close
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(close), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0);
    seccomp_load(ctx);
}

void read_n(int fd, char *buf, int n) {
    int i = 0;
    while (i < n) {
        if (read(fd, buf + i, 1) == 1) {
            i += 1;
        }
    }
}

int main() {
    struct sockaddr_in servaddr = { 0 };
    char player_name[MAX_BUF_SIZE] = { 0 };

    init();
 
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    if (fd == -1) {
        printf("Error during socket creation!\n");
        exit(1);
    }
    
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr(GAME_SERVER_HOST);
    servaddr.sin_port = htons(GAME_SERVER_PORT);
 
    if (connect(fd, (struct sockaddr*)&servaddr, sizeof(servaddr)) != 0) {
        printf("Could not establish connection with server!\n");
        exit(1);
    }

    init_syscall_filter();
    
    printreadline(fd);
    printreadline(fd);
    printreaduntil(fd, ':');
    printreaduntil(fd, ' ');

    int count = read(0, player_name, 511);
    if (count == -1) {
        return 1;
    }

    writeline(fd, player_name, count);
    printreadline(fd);
    // printreadline(fd);

    play_game(fd);

    close(fd);
}
