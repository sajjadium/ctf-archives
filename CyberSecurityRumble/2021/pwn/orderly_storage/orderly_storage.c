#include <unistd.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <threads.h>

// gcc -Wall -Wextra -Werror -pthread -O3 -Wl,-z,relro,-z,lazy -o orderly_storage orderly_storage.c

#if 0
#define DEBUGF(...) printf(__VA_ARGS__)
#else
#define DEBUGF(...) \
    do {            \
    } while (0)
#endif

#define noinline __attribute__((noinline, target("no-sse")))

#define NUM_SLOTS 0x10000

// -------- main --------

static int thread_menu(void *);
static int thread_storage(void *);

int main(void) {
    alarm(30 * 60);

    setbuf(stdout, NULL);

    puts(" _________________");
    puts("< orderly storage >");
    puts(" -----------------");
    puts("");
    puts("available commands:");
    puts("set <idx> <val>     Set value at index");
    puts("get <idx>           Get value at index");
    puts("add <idx> <val>     Add to value at index");
    puts("");

    thrd_t menu, storage;
    thrd_create(&menu, thread_menu, NULL);
    thrd_create(&storage, thread_storage, NULL);
    thrd_join(menu, NULL);
    thrd_join(storage, NULL);
}

// -------- message passing --------

typedef enum {
    msg_kind_set,
    msg_kind_get,
    msg_kind_add,
} msg_kind_t;

typedef struct {
    msg_kind_t kind;
    union {
        struct {
            size_t idx, val;
        } set;
        struct {
            size_t idx;
        } get;
        struct {
            size_t val, idx;
        } add;
    };
} msg_t;

msg_t shared_msg;
volatile bool shared_msg_valid;

noinline static void msg_send(const msg_t *msg) {
    while (shared_msg_valid)
        continue;
    shared_msg = *msg;
    shared_msg_valid = true;
}

noinline static void msg_receive(msg_t *msg) {
    while (!shared_msg_valid)
        continue;
    *msg = shared_msg;
    shared_msg_valid = false;
}

// -------- menu --------

static void bye(void) {
    printf("bye!\n");
    exit(EXIT_SUCCESS);
}

static size_t parse_next_param(char **saveptr) {
    char *tok = strtok_r(NULL, " \n", saveptr);
    if (!tok)
        bye();

    return strtoul(tok, NULL, 10);
}

int thread_menu(void *unused) {
    (void)unused;

    for (;;) {
        char cmd[0x100];
        if (!fgets(cmd, sizeof cmd, stdin))
            bye();

        char *save = NULL;
        char *tok = strtok_r(cmd, " \n", &save);
        if (!tok)
            bye();

        if (!strcmp("set", tok)) {
            size_t idx = parse_next_param(&save);
            size_t val = parse_next_param(&save);

            if (idx < NUM_SLOTS) {
                DEBUGF("sending set %zu %zu\n", idx, val);
                msg_t msg;
                msg.kind = msg_kind_set;
                msg.set.idx = idx;
                msg.set.val = val;
                msg_send(&msg);
            }

        } else if (!strcmp("get", tok)) {
            size_t idx = parse_next_param(&save);

            if (idx < NUM_SLOTS) {
                DEBUGF("sending get %zu\n", idx);
                msg_t msg;
                msg.kind = msg_kind_get;
                msg.get.idx = idx;
                msg_send(&msg);
            }

        } else if (!strcmp("add", tok)) {
            size_t idx = parse_next_param(&save);
            size_t val = parse_next_param(&save);

            if (idx < NUM_SLOTS) {
                DEBUGF("sending add %zu %zu\n", idx, val);
                msg_t msg;
                msg.kind = msg_kind_add;
                msg.add.idx = idx;
                msg.add.val = val;
                msg_send(&msg);
            }

        } else {
            printf("unknown command: ");
            puts(cmd);
            bye();
        }
    }

    return 0;
}

// -------- storage --------

static size_t storage[NUM_SLOTS];

int thread_storage(void *unused) {
    (void)unused;

    for (;;) {
        msg_t msg;
        msg_receive(&msg);

        switch (msg.kind) {

            case msg_kind_set:
                DEBUGF("set: [%zu] = %zu\n", msg.set.idx, msg.set.val);
                storage[msg.set.idx] = msg.set.val;
                break;

            case msg_kind_get:
                DEBUGF("get: [%zu]\n", msg.get.idx);
                printf("%zu\n", storage[msg.get.idx]);
                break;

            case msg_kind_add:
                DEBUGF("add: [%zu] += %zu\n", msg.add.idx, msg.add.val);
                storage[msg.add.idx] += msg.add.val;
                break;
        }
    }

    return 0;
}
