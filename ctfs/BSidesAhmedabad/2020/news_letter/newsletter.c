// gcc -no-pie newsletter.c -o newsletter

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

const char *WELCOME_MESSAGE ="Welcome editor! Feel free to use this as your forum, it's airtight.";
const char *MENU = 
 "\nHi, editor!\n"
 "What do you want to do?\n"
 "\n"
 " 1 - add an article\n"
 " 2 - suggest an edit\n"
 " 3 - apply suggested edit\n"
 " 4 - send to chief editor\n"
 " 5 - read an article\n"
 " 6 - delete an article\n"
 " 7 - exit";

const char *SUGGEST_MENU = 
 "What do you want to do?\n"
 " 1 - insert something\n"
 " 2 - remove something";


typedef struct {
    int secret;
    int length;
    char note[141];
    char signature[64];
} __attribute__((packed)) article_t;

typedef struct {
    int article;
    int type;
    int offset;
    int count;
    char* content; 
} edit_t;

#define INSERT 1
#define DELETE 2

const int ARTICLES = 64;
const int EDITS = 64;

int is_chief_editor = 0;

article_t** articles;
edit_t** edits;
char* signature;


void free_edit(edit_t* edit) {
    if (!edit || edit->type == DELETE) {
        return;
    }

    if (!edit->content) { 
        return;
    }

    free(edit->content);
}

void add_article() {
    char content[141];
    puts("Enter your article:");
    scanf("%140s", content);
    
    for (int i = 0; i < ARTICLES; i++) {
        if (!articles[i]) {
            articles[i] = malloc(sizeof(article_t));
            articles[i]->secret = 0;
            articles[i]->length = strlen(content);
            articles[i]->signature[0] = 0;
            strcpy(articles[i]->note, content);

            printf("Article ID = %d\n", i);
            return;
        }
    }

    puts("No free space available.");
}

void add_edit_insert(int id) {
    puts("Before which character should your edit be pasted?");
    int offset;
    scanf("%d", &offset);

    if (offset < 0 || offset > articles[id]->length) {
        puts("No such offset.");
        return;
    }

    getchar(); 

    puts("Enter your change:");
    char content[141];
    int read = 0;
    while (1) {
        if (read == 141) {
            puts("Too long string.");
            return;
        }
        char next = getchar();
        content[read] = next;
        read += 1;

        if (next == '\n') {
            content[read - 1] = 0;
            break;
        }
    }

    for (int i = 0; i < EDITS; i++) {
        if (!edits[i]) {
            edits[i] = malloc(sizeof(edit_t));
            edits[i]->article = id;
            edits[i]->type = INSERT;
            edits[i]->offset = offset;
            edits[i]->count = read;
            edits[i]->content = malloc(141);
            strcpy(edits[i]->content, content);
            printf("Edit ID = %d\n", i);
            return;
        }
    }

    puts("No free space available.");
}

void add_edit_delete(int id) {
    puts("From which character should the text be deleted?");
    int offset;
    scanf("%d", &offset);

    if (offset < 0 || offset > articles[id]->length) {
        puts("No such offset");
        return;
    }

    puts("How many characters should be deleted?");
    int count;
    scanf("%d", &count);

    if (count <= 0 || offset + count - 1 > articles[id]->length) {
        puts("Not enough characters");
        return;
    }

    for (int i = 0; i < EDITS; i++) {
        if (!edits[i]) {
            edits[i] = malloc(sizeof(edit_t));
            edits[i]->article = id;
            edits[i]->type = DELETE;
            edits[i]->offset = offset;
            edits[i]->count = count;
            printf("Edit ID = %d\n", i);
            return;
        }
    }

    puts("No free space available.");
}

void add_edit() {
    int id;
    puts("Enter article ID to edit:");
    scanf("%d", &id);

    if (id < 0 || id >= ARTICLES || !articles[id]) {
        puts("No such article.");
        return;
    }

    puts(SUGGEST_MENU);
    int choice;
    scanf("%d", &choice);

    switch (choice) {
        case INSERT:
            add_edit_insert(id);
            break;
        case DELETE:
            add_edit_delete(id);
            break;
        default:
            puts("No such option.");
    }
}

void apply_edit() {
    int id;
    puts("Enter edit ID:");
    scanf("%d", &id);

    if (id < 0 || id >= EDITS || !edits[id]) {
        puts("No such edit.");
        return;
    }

    int article = edits[id]->article;

    if (!articles[article]) {
        puts("No such article.");
        return;
    }

    if (edits[id]->type == INSERT) {
        if (articles[article]->signature[0] != 0) {
            puts("Article is approved, can't insert.");
            return;
        }

        int left = edits[id]->offset;
        
        if (left > articles[article]->length) {
            puts("Can't apply this edit.");
        }

        int len = strlen(edits[id]->content);
        if (len + articles[article]->length > 140) {
            puts("Too long.");
            return;
        }

        int new_left = left + len;
        for (int i = 140; i >= new_left; i--) {
            articles[article]->note[i] = articles[article]->note[i - len];
        }

        for (int i = 0; i < len; i++) {
            articles[article]->note[left + i] = edits[id]->content[i];
        }

        articles[article]->length += edits[id]->count;

        free_edit(edits[id]);
        free(edits[id]);
        edits[id] = 0;
        puts("OK!");
    } else {
        int left = edits[id]->offset;
        int right = left + edits[id]->count;

        if (right > articles[article]->length) {
            puts("Can't apply this edit.");
            return;
        }

        articles[article]->length -= edits[id]->count;

        for (int i = left; i < right; i++) {
            articles[article]->note[i] = articles[article]->note[i + (right - left)];
        }

        
        free(edits[id]);
        edits[id] = 0;

        puts("OK!");
    }
}

void sign_article() {
    int id;
    puts("Enter article ID:");
    scanf("%d", &id);

    if (id < 0 || id >= ARTICLES || !articles[id]) {
        puts("No such article.");
        return;
    }

    puts("Sending to chief editor, wait...");
    usleep(2000);
    
    strcpy(articles[id]->signature, signature);
    puts("Article is approved! Thank you!");
}

void read_article() {
    int id;
    puts("Enter article ID:");
    scanf("%d", &id);

    if (id < 0 || id >= ARTICLES || !articles[id]) {
        puts("No such article.");
        return;
    }

    if (articles[id]->secret) {
        puts("You can't see this article.");
        return;
    }

    printf("Your article is: ");
    puts(articles[id]->note);
}

void delete_article() {
    int id;
    puts("Enter article ID:");
    scanf("%d", &id);

    if (id < 0 || id >= ARTICLES || !articles[id]) {
        puts("No such article.");
        return;
    }

    memset(articles[id], NULL, sizeof(article_t*));
}


int menu() {
    puts(MENU);
    printf("> ");
    fflush(stdout);
    int option;
    int ok = scanf("%d", &option);
    
    if (!ok) {
        return 0;
    }

    switch (option) {
        case 1:
            add_article();
            break;
        case 2:
            add_edit();
            break;
        case 3:
            apply_edit();
            break;
        case 4:
            sign_article();
            break;
        case 5:
            read_article();
            break;
        case 6:
            delete_article();
            break;
        case 7:
            return 0;
        default:
            puts("Something went wrong!\n");
    }

    return 1;
}


void init_app() {
    articles = malloc(ARTICLES * sizeof(article_t*));
    memset(articles, 0, ARTICLES * sizeof(article_t*));

    edits = malloc(EDITS * sizeof(edit_t*));
    memset(edits, 0, EDITS * sizeof(edit_t*));
    FILE *fp;    
    fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        puts("flag not found. Please contact the admin.");
        exit(1);
    }

    signature = malloc(64);
    fscanf(fp, "%63s", signature);
    fclose(fp);

    while (menu());
    puts("Thank you for your work! See you tomorrow!");

    for (int i = 0; i < ARTICLES; i++) {
        if (articles[i]) {
            free(articles[i]);
        }
    }
    free(articles);

    for (int i = 0; i < EDITS; i++) {
        if (edits[i]) {
            free_edit(edits[i]);
            free(edits[i]);
        }
    }
    free(edits);
    free(signature);
}

int main(int argc, char** argv) {
    setbuf(stdout, NULL);
    alarm(30);

    puts(WELCOME_MESSAGE);
    init_app();
    return 0;
}
