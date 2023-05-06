#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "alloc.h"

#define BUF_SIZE 128

// Compilation: gcc -Wall -g -fno-stack-protector -z execstack -o password passwd.c alloc.c alloc.h

typedef struct pass {
        char pass[BUF_SIZE];
        struct pass *next;
        struct pass *prev;
        unsigned long id;
} pass_t;

void print_pass(pass_t *n) {
        printf("Password #%ld\n", n->id);
        printf(n->pass);
}

unsigned long generate_id(pass_t *head) {
        pass_t *tmp = NULL;
        unsigned long id = 0;
        id = rand();

        for(tmp = head; tmp != NULL; tmp = tmp->next) {
                if(id == tmp->id) {
                        id = generate_id(head);
                        break;
                }
        }

        return id;
}

void new_pass(pass_t **head) {
        pass_t *new = NULL;

        new = heap_alloc(sizeof(pass_t));
        if(new == NULL) {
                printf("heap_alloc() failed.");
                exit(1);
        }

        new->next = *head;
        if(*head != NULL) {
                (*head)->prev = new;
        }
        *head = new;
        new->id = generate_id(*head);

        printf("Enter the password (%d max characters): ", BUF_SIZE);
        fgets(new->pass, BUF_SIZE, stdin);

        printf("Password created with ID #%lu.\n", new->id);
}

void print_id(unsigned long id, pass_t *head) {
        pass_t *tmp = head;
        while(tmp != NULL && tmp->id != id) {
                tmp = tmp->next;
        }

        if(tmp != NULL) {
                print_pass(tmp);
        } else {
                printf("Invalid ID.\n");
        }
}

void modify_id(unsigned long id, pass_t *head) {
        pass_t *tmp = head;
        while(tmp != NULL && tmp->id != id) {
                tmp = tmp->next;
        }
        if(tmp != NULL) {
                printf("Enter the modified password (%d max characters): ", BUF_SIZE);
                fgets(tmp->pass, 1000, stdin);
        } else {
                printf("Invalid ID.\n");
        }
}

void del_id(unsigned long id, pass_t **head) {
        pass_t *tmp = *head;
        while(tmp != NULL) {
                if(tmp->id == id) {
                        if(tmp->prev != NULL) {
                                tmp->prev->next = tmp->next;
                        }
                        if(tmp->next != NULL) {
                                tmp->next->prev = tmp->prev;
                        }
                        if(tmp == *head) {
                                *head = (*head)->next;
                        }
                        heap_free(tmp);
                        break;
                }
                tmp = tmp->next;
        }
}

void del_all(pass_t *head) {
        pass_t *tmp = NULL;
        while(head != NULL) {
                tmp = head;
                head = head->next;
                heap_free(tmp);
        }
}

void print_cmds() {
        printf("Available commands:\n");
        printf("new: Create a new password.\n");
        printf("print <id>: Prints out the password with the given ID.\n");
        printf("del <id>: Deletes the password with the given ID.\n");
        printf("modify <id>: Modifies the password with the given ID.\n");
        printf("quit: Stop the program.\n");
}

void command_line() {
        unsigned long id = 0;
        char stop = 0;
        char buf[BUF_SIZE] = {0};
        pass_t *head = NULL;

        while(!stop) {
                printf("> ");
                fgets(buf, BUF_SIZE, stdin);
                if(strncmp(buf, "new", 3) == 0) {
                        new_pass(&head);
                } else if(strncmp(buf, "print ", 6) == 0) {
                        sscanf(buf+6, "%lu", &id);
                        print_id(id, head);
                } else if(strncmp(buf, "del ", 4) == 0) {
                        sscanf(buf+4, "%lu", &id);
                        del_id(id, &head);
                } else if(strncmp(buf, "modify ", 7) == 0) {
                        sscanf(buf+7, "%lu", &id);
                        modify_id(id, head);
                } else if(strncmp(buf, "quit", 4) == 0 || strncmp(buf, "q\n", 2) == 0) {
                        stop = 1;
                } else {
                        printf("Invalid command.\n");
                }
        }

        printf("Ending program.\n");
        del_all(head);
        head = NULL;
}

void create_account(char *username) {
        printf("Hello, welcome to the world's greatest password manager!\n");
        printf("This password manager is so amazing that it uses a custom\n");
        printf("heap implementation! No hacker will ever be successful in\n");
        printf("conducting a heap overflow against this application (let\n");
        printf("alone ever obtain a shell)! It is impossible to hack into\n");
        printf("this application, so you shouldn\'t even bother trying!\n\n");

        printf("To create a new account, please enter a username: ");
        fgets(username, BUF_SIZE, stdin);
        username[strlen(username)-1] = '\0';
        printf("A new account for %s has been created.\n\n", username);
}

int main(int argc, char **argv) {
        char username[BUF_SIZE] = {0};
        srand((unsigned) time(0));

        create_account(username);
        print_cmds();
        command_line();

        return 0;
}
