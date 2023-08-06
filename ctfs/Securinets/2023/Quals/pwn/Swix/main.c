// gcc main.c -o main -m32 -no-pie

#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/sendfile.h>
#include <string.h>

#define MAX_FRIENDS 1

typedef struct user{
    char username[8];
    char description[256];
    int id;
    int age;
    char password[32-4];
    struct user **friends;
    int friendCount;
} user;

user u;

char superSecretMessage[] = "\x0c\x62\x28\x65\x36\x24\x23\x20\x64\x65\x0c\x65\x32\x2c\x36\x2d";

int usedHack = 0;

// Files to use
int uname, age, logo, menu, f2, f3;

// Code
void initStuff(){
    uname = open("uname", O_RDONLY);
    age = open("age", O_RDONLY);
    logo = open("logo", O_RDONLY);
    menu = open("menu", O_RDONLY);
    f2 = open("msg2", O_RDONLY);
    f3 = open("msg3", O_RDONLY);
    
    u.friendCount = 0;
    u.friends = (user**) malloc(sizeof(user*)*MAX_FRIENDS);
}

char* SuperHardEncoding(char* s){
    
    for(int i=0; i<16; i++){
        s[i] = s[i] ^ 69;
    }
    return s;
}

void showMsg(int fd, size_t size){
    off_t off = 0;
    sendfile(1, fd, &off, size);
}

void addFriend(){
    if(uname == -1){
        exit(0);
    }
    
    if(u.friendCount >= MAX_FRIENDS){
        return;
    }
    
    u.friends[u.friendCount] = (user *)malloc(sizeof(user));
    
    showMsg(uname, 10);
    read(0, u.friends[u.friendCount]->username, 8);
    
    u.friendCount++;
}

void editFriend(){
    if(uname == -1){
        exit(0);
    }
    
    if(u.friendCount == 0){
        return;
    }
    
    char idx;
    read(0, &idx, 1);
    
    int id = (int)(idx - '0');
    if(id >= u.friendCount){
        return;
    }
    
    if(id > 9 || id < 0){
        return;
    }
    
    showMsg(uname, 10);
    read(0, u.friends[id]->username, 8);
}

void getFriendAdr(){
    if(f2 == -1 || f3 == -1){
        exit(0);
    }
    if(usedHack == 1) return;
    usedHack = 1;
    
    char idx;
    read(0, &idx, 1);
    
    int id = (int)(idx - '0');
    if(id >= u.friendCount){
        return;
    }
    
    if(id > 9 || id < 0){
        return;
    }
    
    unsigned int hack = (unsigned int)u.friends[id];
    while(hack){
        if(hack&1){
            showMsg(f2, 26);
        }
        else showMsg(f3, 1);
        
        hack = hack / 2;
    }
}

void magicMove(unsigned int *p){
    read(0, p, 16);
}

int readInt(){
    char tmp[11] = {0};

    read(0, tmp, 10);
    return atoi(tmp);
}

void setCreds(){
    if(uname == -1 || age == -1){
        exit(0);
    }
    
    showMsg(uname, 10);
    read(0, u.username, 8);
    
    showMsg(age, 5);
    u.age = readInt();
}

int main(){
    unsigned int *p;
    p = &p;
    p = (unsigned int*)((unsigned int)p+0x20);
    
    initStuff();
    
    if(logo == -1 | menu == -1){
        return 1;
    }
    
    showMsg(logo, 3201);
    char choice;
    
    while(choice != '6'){
        showMsg(menu, 95);
        
        read(0, &choice, 1);
        switch(choice){
            case '1':{
                setCreds();
                break;
            }
            
            case '2':{
                addFriend();
                break;
            }
            
            case '3':{
                editFriend();
                break;
            }
            
            case '4':{
                getFriendAdr();
                break;
            }
            
            case '5':{
                magicMove(p);
                break;
            }
            
            case '6':{
                break;
            }
            
            default:{
                exit(0);
            }
        }
    }
    
    SuperHardEncoding(superSecretMessage);
    puts(superSecretMessage);
    SuperHardEncoding(superSecretMessage);
    p[2] = 0xdeadbeef;
}
