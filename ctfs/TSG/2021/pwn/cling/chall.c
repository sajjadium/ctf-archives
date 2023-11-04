#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <cling/Interpreter/Interpreter.h>
#include <cling/Interpreter/Value.h>

// I don't want you to create too much mmaps...
#define N_CREATE 10

typedef unsigned long long u64;

unsigned long long *buf = NULL;
u64 n_elem = 0;

u64 n_create = 0;

u64 get_num() {
    u64 c;
    if (scanf("%llu", &c) != 1)
        exit(-1);
    return c;
}

u64 get_yes_no() {
    char buf[8];
    if (scanf("%7s", buf) != 1)
        exit(-1);
    return buf[0] == 'Y' || buf[0] == 'y';
}

void readn(char *buf, unsigned size) {
    unsigned cnt = 0;
    for (unsigned i = 0; i < size; i++) {
        unsigned x = read(0, buf + i, 1);
        cnt += x;
        if (x != 1 || buf[cnt - 1] == '\n') break;
    }
    if (cnt == 0) exit(-1);
    if (buf[cnt - 1] == '\n') buf[cnt - 1] = '\x00';
}

void setup() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void create() {
    if (n_create > N_CREATE) {
        puts("too many creation");
        return;
    }
    printf("size? >");
    unsigned size = get_num();
    if (0 == size || size > (0x1000/sizeof(unsigned long long))) {
        puts("too big");
        return;
    }
    n_create++;
    buf = (unsigned long long *)mmap(NULL, 0x1000 , PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    n_elem = size;
    if ((long long int)buf == -1) {
        puts("fail");
        n_elem = 0;
        buf = NULL;
        return;
    }
    for (int i = 0; i < n_elem; i++) {
        if (scanf("%llu", &buf[i]) != 1) return;
    }
}

void protect() {
    u64 prot = PROT_NONE;
    printf("read? >");
    if (get_yes_no()) {
        puts("yes read");
        prot |= PROT_READ;
    }
    printf("write? >");
    if (get_yes_no()) {
        prot |= PROT_WRITE;
    }
    printf("exec? >");
    if (get_yes_no()) {
        prot |= PROT_EXEC;
    }
    int ret = mprotect(buf, 0x1000, prot);
    if (ret == -1) {
        puts("fail");
        n_elem = 0;
        buf = NULL;
    }
}

void del() {
    int ret = munmap(buf, 0x1000);
    if (ret == -1) {
        puts("fail");
        n_elem = 0;
        buf = NULL;
    }
}

int func_set = 0;
void set_map() {
    char expr[8192];
    char func[8492];
    if (!func_set) {
        printf("Give me your map function body > ");
        scanf("%8191s", expr);
        for (int i = 0; i < strlen(expr); i++) {
            if (expr[i] == 'x' ||
                    ('0' <= expr[i] && expr[i] <= '9') ||
                    expr[i] == ' ' ||
                    expr[i] == '+' ||
                    expr[i] == '-' ||
                    expr[i] == '*' ||
                    expr[i] == '/' ||
                    expr[i] == '?' ||
                    expr[i] == ':') continue;
            puts("wrong format");
            return;
        }
        sprintf(func, "unsigned long map_func(unsigned long x) {return %s;}", expr);
        gCling->process(func);

        cling::Value v;
        auto ret = gCling->evaluate("map_func(42)", v);
        if (ret == 0) {
            printf("map_func(42) = %llu\n", v.getULL());
            func_set = 1;
        }
    } else {
        puts("the map function has already been registered.");
    }
}
void run_map() {
    char expr[0x2000];
    if (func_set) {
        cling::Value v;
        if (buf == NULL || n_elem == 0) return;
        for (unsigned i = 0; i < n_elem; i++) {
            sprintf(expr, "map_func(%lluULL)", buf[i]);
            gCling->evaluate(expr, v);
            unsigned long long result = v.getULL();
            buf[i] = result;
        }
    } else {
        puts("no map function has been registered yet.");
    }
}

u64 menu() {
    puts("---------------");
    puts("1. create");
    puts("2. protect");
    puts("3. delete");
    puts("4. set_map");
    puts("5. run_map");
    puts("6. set_reduce");
    puts("7. run_reduce");
    puts("8. show_result");
    puts("---------------");
    printf("> ");
    return get_num();
}

int mymain(void) {
    setup();
    while (1) {
        unsigned cmd = menu();
        switch (cmd) {
            case 1:
                create();
                break;
            case 2:
                protect();
                break;
            case 3:
                del();
                break;
            case 4:
                set_map();
                break;
            case 5:
                run_map();
                break;
            case 6:
            case 7:
            case 8:
                puts("not implemented :p");
                break;
            default:
                puts("bye");
                exit(0);
        }
    }
    return 0;
}

mymain();
