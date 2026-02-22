#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

// gcc chal.c -o chal -fno-stack-protector --debug

typedef struct {
    int id;
    char name[50];
    char password[64];
    int (*on_disconnect)(const char *, ...);
} AgentData;

typedef struct {
    int message_id;
    int user_id;
    char content[256];
} Message;

AgentData login_agent;

void crash_handler(int signum){
    fprintf(stderr, "\033[H\033[2J");
    fprintf(stderr, "Crash detected! Handling crash...\n");
    fprintf(stderr, "The agent system has encountered a critical error and will terminate.\n");
    fprintf(stderr, "=== AGENT SYSTEM CRASH ===\n");
    fprintf(stderr, "Agent name: %s\n", login_agent.name);
    fprintf(stderr, "Password: %s\n", login_agent.password);
    fprintf(stderr, "Disconnect handler: %p\n", (void *)login_agent.on_disconnect);
    fprintf(stderr, "System Restarting...\n\n\n");
    main();
    exit(EXIT_FAILURE);
}

AgentData find_user_by_id(int user_id){
    return login_agent;
}

void init(){
    signal(SIGSEGV, (void *)crash_handler);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    printf("Service initialized.\n");
}

int menu(){
    printf("Here are your options: \n");
    printf("1. Add a message\n");
    printf("2. Change password\n");
    printf("3. Logout\n");
    printf("> ");
    int choice;
    scanf("%d", &choice);
    return choice;
}

int login(){
    printf("Hello sir, please login to continue.\n");
    printf("Username: ");
    scanf("%49s", login_agent.name);
    printf("Password: ");
    scanf("%63s", login_agent.password);
    login_agent.id = 1337;
    login_agent.on_disconnect = puts;
    printf("Welcome, %s!\n\n", login_agent.name);
    return login_agent.id;
}

void add_message(int user_id){
    Message msg;
    msg.user_id = user_id;
    printf("Enter your message: ");
    getchar();
    gets(msg.content);
    printf("Message added for user %d: %s\n\n", msg.user_id, msg.content);
}

void change_password(int user_id){
    printf("Enter new password: ");
    AgentData user = find_user_by_id(user_id);
    scanf("%63s", user.password);
    printf("Password changed for user %s\n\n", user.name);
}

void logout(int user_id){
    AgentData user = find_user_by_id(user_id);
    user.on_disconnect("User logged out.");
    printf("Goodbye, %s!\n", user.name);
    exit(0);
}

int main() {
    init();
    int id = login();
    while(1){
        switch(menu()){
            case 1:
                add_message(id);
                break;
            case 2:
                change_password(id);
                break;
            case 3:
                logout(id);
                break;
            default:
                printf("Invalid option.\n");
                break;
        }
    }
    return 0;
}
