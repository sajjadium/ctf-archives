#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include "flask.h"

int num_flasks;
static pid_t *flasks;
static int *mixing;

// arrays of pipes for communication between flasks and main
static int (*to_flask)[2];
static int (*to_main)[2];

static void proc_flask(int id) {
    int in_fd = to_flask[id][0];
    int out_fd = to_main[id][1];

    char **argv = calloc(MAX_ARGC, sizeof(*argv));
    struct request *req = malloc(MAX_REQ);

    int i;
    char *arg;

    // each flask has its own process group for easy signal management
    setsid();

    // stdin being open causes funky things to happen
    close(STDIN_FILENO);
    dup2(out_fd, STDOUT_FILENO);
    dup2(out_fd, STDERR_FILENO);

    while (read(in_fd, req, MAX_REQ) != -1) {
        switch (req->cmd) {
        case CMD_ADD:
            arg = malloc(req->len + 1);
            memcpy(arg, req->arg, req->len);
            arg[req->len] = '\0';

            if (argv[req->idx])
                free(argv[req->idx]);
            argv[req->idx] = arg;

            // if we set an upper arg, we just put empty string for lower args
            i = req->idx;
            while (i >= 0 && argv[i] == NULL) {
                argv[i] = strdup("");
                i--;
            }
            break;
        case CMD_MIX:
            setuid(1000);
            setgid(1000);

            execvp(argv[0], argv);
            break;
        default:
            fprintf(stderr, "Invalid command!\n");
        }
    }

    exit(EXIT_FAILURE);
}

// initialize flask pool 
void init_flasks(int n) {
    flasks = malloc(sizeof(*flasks) * n);
    mixing = malloc(sizeof(*mixing) * n);
    to_flask = malloc(sizeof(*to_flask) * n);
    to_main = malloc(sizeof(*to_main) * n);

    // create 2 pipes for bidirectional communication with each flask
    // each flask knows which pipes to use based on index passed to it
    for (int i = 0; i < n; i++) {
        pipe2(to_flask[i], O_DIRECT);
        pipe2(to_main[i], O_NONBLOCK);
    }

    // create flasks
    for (int i = 0; i < n; i++) {
        flasks[i] = fork();
        if (flasks[i] == 0)
            proc_flask(i);
    }

    num_flasks = n;
}

void clean_flasks(void) {
    for (int i = 0; i < num_flasks; i++) {
        kill(-flasks[i], SIGKILL);
    }
}

// the ID passed in the below functions is from user perspective
// we need to convert to index by subtracting 1

void flask_add(int id, int i, const char *arg, size_t n) {
    id -= 1;
    i -= 1;

    // can't add if we are mixing
    if (mixing[id])
        return;

    struct request *req = malloc(sizeof(*req) + n);
    req->cmd = CMD_ADD;
    req->idx = i;
    req->len = n;
    memcpy(req->arg, arg, n);

    write(to_flask[id][1], req, sizeof(*req) + n);
    free(req);
}

void flask_mix(int id) {
    id -= 1;

    // can't mix if we are already mixing
    if (mixing[id])
        return;

    struct request req = { .cmd = CMD_MIX };
    write(to_flask[id][1], &req, sizeof(req));
    mixing[id] = 1;
}

// read flask output from respective to_main pipe
void flask_empty(int id) {
    char buf[256];
    int n;

    id -= 1;
    mixing[id] = 0;

    // print output until we have nothing left
    puts("---- Contents ---- ");
    while ((n = read(to_main[id][0], buf, sizeof(buf))) != -1) {
        fwrite(buf, sizeof(char), n, stdout);
    }
    puts("");

    // kill flask and spawn new one
    kill(-flasks[id], SIGKILL);
    while (waitpid(-flasks[id], NULL, WNOHANG) != -1);

    flasks[id] = fork();
    if (flasks[id] == 0)
        proc_flask(id);
}
