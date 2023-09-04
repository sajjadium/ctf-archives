#include <stdio.h>
#include <stdarg.h>
#include <inttypes.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

#define MESSAGE_LEN 1024
#define USERPASS_LEN 128

#define MAX(x,y) (((x) >= (y)) ? (x) : (y))

typedef enum {
    TAG_RES_MSG,
    TAG_RES_ERROR,
    TAG_INPUT_REQ,
    TAG_INPUT_ANS,
    TAG_COMMAND,
    TAG_STR_PASSWORD,
    TAG_STR_FROM,
    TAG_STR_MESSAGE
} tag_t;

typedef struct {
    tag_t tag;
    unsigned long len;
} taglen_t;

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win() {
    system("cat flag.txt");
}

int read_taglen(FILE* fp, taglen_t* tlv) {
    char tmpbuf[12];
    fread(tmpbuf, 1, 12, fp);

    tlv->tag = *((tag_t*)&tmpbuf[0]);
    tlv->len = *((unsigned long*)&tmpbuf[4]);
}

void pack_taglen(tag_t tag, unsigned long len, char buf[12]) {
    *(tag_t*)&buf[0] = tag;
    *(unsigned long*)&buf[4] = len;
}

void print_tlv(tag_t tag, const char* fmt, ...) {
    char msg[0x1000];
    va_list args;
    va_start(args, fmt);
    vsprintf(msg, fmt, args);
    va_end(args);

    int len = strlen(msg);
    char tmpbuf[12];
    pack_taglen(tag, len, tmpbuf);
    fwrite(tmpbuf, 1, 12, stdout);
    fwrite(msg, 1, len, stdout);
}

FILE* get_user_save_fp(char username[USERPASS_LEN], const char* mode) {
    char fname[USERPASS_LEN + 6];

    snprintf(fname, USERPASS_LEN + 6, "/tmp/%s", username);
    FILE* fp = fopen(fname, mode);

    return fp;
}

void register_user() {
    char tmpbuf[USERPASS_LEN];
    char tmpbuf2[12];
    taglen_t tl;

    print_tlv(TAG_INPUT_REQ, "username");
    read_taglen(stdin, &tl);
    if(tl.tag != TAG_INPUT_ANS || tl.len >= USERPASS_LEN) {
        print_tlv(TAG_RES_ERROR, "invalid username input");
        return;
    }
    fread(tmpbuf, 1, tl.len, stdin);
    tmpbuf[tl.len] = '\0';

    FILE* fp = get_user_save_fp(tmpbuf, "r");
    if(fp == 0) {
        fp = get_user_save_fp(tmpbuf, "w+");

        print_tlv(TAG_INPUT_REQ, "password");
        read_taglen(stdin, &tl);
        if(tl.tag != TAG_INPUT_ANS || tl.len >= USERPASS_LEN) {
            print_tlv(TAG_RES_ERROR, "invalid password input");
            return;
        }
        fread(tmpbuf, 1, tl.len, stdin);

        pack_taglen(TAG_STR_PASSWORD, tl.len, tmpbuf2);
        fwrite(tmpbuf2, 1, 12, fp);
        fwrite(tmpbuf, 1, tl.len, fp);
        fflush(fp);

        print_tlv(TAG_RES_MSG, "user registered");
    } else {
        print_tlv(TAG_RES_ERROR, "user already exists");
    }
}

FILE* handle_auth(char username[USERPASS_LEN]) {
    char tmpbuf[USERPASS_LEN];
    char tmpbuf2[USERPASS_LEN];
    taglen_t tl;

    FILE* fp = get_user_save_fp(username, "r");

    if(fp == 0) {
        print_tlv(TAG_RES_ERROR, "user does not exist");
        return 0;
    } else {
        print_tlv(TAG_INPUT_REQ, "password");
        read_taglen(stdin, &tl);
        if(tl.tag != TAG_INPUT_ANS || tl.len >= USERPASS_LEN) {
            print_tlv(TAG_RES_ERROR, "invalid password input");
            return 0;
        }
        unsigned long t1 = tl.len;
        fread(tmpbuf, 1, tl.len, stdin);

        read_taglen(fp, &tl);
        if(tl.tag != TAG_STR_PASSWORD || tl.len >= USERPASS_LEN) {
            print_tlv(TAG_RES_ERROR, "corrupted user file, got invalid taglen %d %lld", tl.tag, tl.len);
            return 0;
        }
        fread(tmpbuf2, 1, tl.len, fp);

        if(memcmp(tmpbuf, tmpbuf2, MAX(t1, tl.len)) != 0) {
            print_tlv(TAG_RES_ERROR, "incorrect password");
            return 0;
        }

        return fp;
    }
}

void view_mail() {
    char tmpbuf[USERPASS_LEN + MESSAGE_LEN + 16];
    char tmpbuf2[USERPASS_LEN];
    taglen_t tl;

    print_tlv(TAG_INPUT_REQ, "username");
    read_taglen(stdin, &tl);
    if(tl.tag != TAG_INPUT_ANS || tl.len >= USERPASS_LEN) {
        print_tlv(TAG_RES_ERROR, "invalid username input");
        return;
    }
    fread(tmpbuf, 1, tl.len, stdin);
    tmpbuf[tl.len] = '\0';

    FILE* fp = handle_auth(tmpbuf);
    if(fp == 0) return;

    read_taglen(fp, &tl);
    if(feof(fp)) {
        print_tlv(TAG_RES_MSG, "no mail");
        return;
    }
    unsigned long t1 = tl.len;
    if(tl.tag != TAG_STR_FROM || t1 >= USERPASS_LEN) {
        print_tlv(TAG_RES_ERROR, "mail invalid from");
        return;
    }
    memcpy(tmpbuf, "from: ", 6);
    fread(tmpbuf + 6, 1, t1, fp);
    tmpbuf[6 + t1] = '\n';

    read_taglen(fp, &tl);
    unsigned long t2 = tl.len;
    if(tl.tag != TAG_STR_MESSAGE || (t1 + t2) >= USERPASS_LEN + MESSAGE_LEN) {
        print_tlv(TAG_RES_ERROR, "mail invalid message");
        return;
    }
    memcpy(tmpbuf + 6 + t1 + 1, "message: ", 9);
    fread(tmpbuf + 6 + t1 + 1 + 9, 1, t2, fp);

    pack_taglen(TAG_RES_MSG, t1 + t2 + 16, tmpbuf2);
    fwrite(tmpbuf2, 1, 12, stdout);
    fwrite(tmpbuf, 1, t1 + t2 + 16, stdout);
    fflush(stdout);
}

void send_mail() {
    char tmpbuf[MESSAGE_LEN];
    char tmpbuf2[USERPASS_LEN];
    taglen_t tl;

    print_tlv(TAG_INPUT_REQ, "username");
    read_taglen(stdin, &tl);
    unsigned long t1 = tl.len;
    if(tl.tag != TAG_INPUT_ANS || tl.len >= USERPASS_LEN) {
        print_tlv(TAG_RES_ERROR, "invalid username input");
        return;
    }
    fread(tmpbuf, 1, tl.len, stdin);
    tmpbuf[tl.len] = '\0';

    if(handle_auth(tmpbuf) == 0) return;

    print_tlv(TAG_INPUT_REQ, "recipient");
    read_taglen(stdin, &tl);
    if(tl.tag != TAG_INPUT_ANS || tl.len >= USERPASS_LEN) {
        print_tlv(TAG_RES_ERROR, "invalid recipient input");
        return;
    }
    fread(tmpbuf2, 1, tl.len, stdin);
    tmpbuf2[tl.len] = '\0';
    FILE* fp = get_user_save_fp(tmpbuf2, "a+");

    pack_taglen(TAG_STR_FROM, tl.len, tmpbuf+USERPASS_LEN);
    fwrite(tmpbuf+USERPASS_LEN, 1, 12, fp);
    fwrite(tmpbuf, 1, t1, fp);

    print_tlv(TAG_INPUT_REQ, "message");
    read_taglen(stdin, &tl);
    if(tl.tag != TAG_INPUT_ANS || tl.len >= MESSAGE_LEN) {
        print_tlv(TAG_RES_ERROR, "invalid message input");
        return;
    }
    fread(tmpbuf, 1, tl.len, stdin);

    pack_taglen(TAG_STR_MESSAGE, tl.len, tmpbuf2);
    fwrite(tmpbuf2, 1, 12, fp);
    fwrite(tmpbuf, 1, tl.len, fp);
    fflush(fp);

    print_tlv(TAG_RES_MSG, "message sent");
}

int main() {
    init();
    puts("binary mail v0.1.0");
    taglen_t cmd_tl;
    char tmpbuf[128];

    while(1) {
        read_taglen(stdin, &cmd_tl);
        if(cmd_tl.tag != TAG_COMMAND || cmd_tl.len >= 128) {
            print_tlv(TAG_RES_ERROR, "invalid command");
            continue;
        }
        fread(tmpbuf, 1, cmd_tl.len, stdin);
        if(strncmp(tmpbuf, "register", 8) == 0) {
            register_user();
        }
        if(strncmp(tmpbuf, "view_mail", 9) == 0) {
            view_mail();
        }
        if(strncmp(tmpbuf, "send_mail", 9) == 0) {
            send_mail();
        }
    }
}
