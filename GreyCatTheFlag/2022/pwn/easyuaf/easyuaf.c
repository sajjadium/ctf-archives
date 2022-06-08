#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BANNER "NameCard Printing Service v0.1"
#define CAPACITY 128

void ezflag()
{
    system("cat ./flag.txt");
}

typedef struct person
{
    char name[24];
    int id;
    int age;
    int personal_num;
    int business_num;
} person;

typedef struct org
{
    char name[24];
    int id;
    void (*display)(struct org*, struct person*);
} org;

person* persons[CAPACITY];
org* orgs[CAPACITY];

void display1(org* org, person *person)
{
    puts("-------------------------------------");
    printf("*** Org:  %-8s  %d ***\n", org->name, org->id);
    printf("--- Name: %s\n", person->name);
    printf("--- ID:   %d\n", person->id);
    printf("--- Age:  %d\n", person->age);
    printf("--- Personal Contact:  %d\n", person->personal_num);
    printf("--- Business Contact:  %d\n", person->business_num);
    puts("-------------------------------------");
}

void display2(org* org, person *person)
{
    puts("-------------------------------------");
    printf("=== Org:  %-8s  %d ===\n", org->name, org->id);
    printf("+++ Name: %s\n", person->name);
    printf("+++ ID:   %d\n", person->id);
    printf("+++ Age:  %d\n", person->age);
    printf("+++ Personal Contact:  %d\n", person->personal_num);
    printf("+++ Business Contact:  %d\n", person->business_num);
    puts("-------------------------------------");
}

void display3(org* org, person *person)
{
    puts("-------------------------------------");
    printf("### Org:  %-8s  %d ###\n", org->name, org->id);
    printf(">>> Name: %s\n", person->name);
    printf(">>> ID:   %d\n", person->id);
    printf(">>> Age:  %d\n", person->age);
    printf(">>> Personal Contact:  %d\n", person->personal_num);
    printf(">>> Business Contact:  %d\n", person->business_num);
    puts("-------------------------------------");
}

void usage()
{
    puts("---------------------");
    puts("1. New person");
    puts("2. New org");
    puts("3. Delete org");
    puts("4. Print name card");
    puts("5. Exit");
    puts("---------------------");
}

void prompt()
{
    printf("> ");
}

void readstr(char* dest, int len)
{
    fgets(dest, len, stdin);
    if (dest[strlen(dest)-1] == '\n') dest[strlen(dest)-1] = 0;
}

int readint()
{
    char input[256]; fgets(input, 256, stdin);
    if (input[0] == '\n') input[0] = ' ';
    return strtol(input, 0, 10);
}

void new_person()
{
    person *res = (person*) malloc(sizeof(person));
    // printf("res: %p\n", res);

    while (1)
    {
        printf("ID (0-%d): ", CAPACITY-1);
        res->id = readint();
        if (res->id < 0 || res->id >= CAPACITY) puts("Invalid ID");
        else if (persons[res->id] != 0)
            printf("ID %d is already used by another person. Choose a different ID.\n", res->id);
        else break;
    }

    printf("Name (max 23 chars): ");
    readstr(res->name, 24);

    printf("Age: ");
    res->age = readint();

    printf("Personal Contact Number: ");
    res->personal_num = readint();

    printf("Business Contact Number: ");
    res->business_num = readint();

    persons[res->id] = res;
}

void new_org()
{
    org *res = (org*) malloc(sizeof(org));
    // printf("res: %p\n", res);

    while (1)
    {
        printf("ID (0-%d): ", CAPACITY-1);
        res->id = readint();
        if (res->id < 0 || res->id >= CAPACITY) puts("Invalid ID");
        else if (orgs[res->id] != 0)
            printf("ID %d is already used by another org. Choose a different ID.\n", res->id);
        else break;
    }

    printf("Name (max 23 chars): ");
    readstr(res->name, 24);

    int style;
    while (1)
    {
        printf("Style (1-3): ");
        style = readint();
        if (style >= 1 && style <= 3) break;
        puts("Invalid style.");
    }

    if (style == 1) res->display = display1;
    if (style == 2) res->display = display2;
    if (style == 3) res->display = display3;

    orgs[res->id] = res;
}

void delete_org()
{
    printf("ID (0-%d): ", CAPACITY-1);
    int id = readint();
    if (id < 0 || id >= CAPACITY) puts("Invalid ID");
    else if (orgs[id] == 0)
        printf("No org created with ID %d.\n", id);
    else
    {
        free(orgs[id]);
        printf("Deleted org %d.\n", id);
    }
}

void print_card()
{
    int org_id;
    while (1)
    {
        printf("Org ID (0-%d): ", CAPACITY-1);
        org_id = readint();
        if (org_id < 0 || org_id >= CAPACITY) puts("Invalid org ID");
        else if (orgs[org_id] == 0)
            printf("No org created with ID %d. Choose a different ID.\n", org_id);
        else break;
    }

    int person_id;
    while (1)
    {
        printf("Person ID (0-%d): ", CAPACITY-1);
        person_id = readint();
        if (person_id < 0 || person_id >= CAPACITY) puts("Invalid person ID");
        else if (persons[person_id] == 0)
            printf("No person created with ID %d. Choose a different ID.\n", org_id);
        else break;
    }

    org *o = orgs[org_id];
    person *p = persons[person_id];

    // printf("display func @ %p\n", o->display);
    o->display(o, p);
}

void reset()
{
    memset(persons, 0, sizeof(persons));
    memset(orgs, 0, sizeof(orgs));
}

void setup_io()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main()
{
    // org* o1 = (org*)malloc(sizeof(org));
    // person* p1 = (person*)malloc(sizeof(person));
    // printf("o1: %p\n", o1);
    // printf("p1: %p\n", p1);
    // free(o1);
    // person* p2 = (person*)malloc(sizeof(person));
    // printf("p2: %p\n", p2);

    reset();

    setup_io();
    puts(BANNER);
    usage();

    // printf("%d %d\n", sizeof(org), sizeof(person));

    int opt;
    do {
        prompt();
        opt = readint();

        switch (opt)
        {
        case 1:
            new_person();
            break;
        case 2:
            new_org();
            break;
        case 3:
            delete_org();
            break;
        case 4:
            print_card();
            break;
        default:
            break;
        }
    } while (opt != 5);

    puts("Thanks for using this service. Please come again next time.");

    return 0;
}