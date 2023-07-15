#include <fcntl.h>
#include <signal.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define ARR_SIZE 0x10
#define CMD_WAIT 0
#define CMD_EDIT 1
#define CMD_SHOW 2
#define CMD_EXIT 3

#define DEFINE_SETTER(type, name)                         \
  void io_set_##name(type *name) {                        \
    io_set(offsetof(ArrayIO, name), name, sizeof(type));  \
  }

#define DEFINE_SETTER_CONST(type, name)                   \
  void io_set_##name(type name) {                         \
    io_set(offsetof(ArrayIO, name), &name, sizeof(type)); \
  }

#define DEFINE_GETTER(type, name)                          \
  type io_get_##name(void) {                               \
    type name;                                             \
    io_get(offsetof(ArrayIO, name), &name, sizeof(type));  \
    return name;                                           \
  }

#define WAIT_RESPONSE() \
  while (io_get_command() != CMD_WAIT) usleep(100000);

#define WAIT_REQUEST() \
  while (io_get_command() == CMD_WAIT) usleep(100000);

int verbose;

typedef struct {
  int command;
  ssize_t index;
  size_t value;
} ArrayIO;

int mapfd;
char mapname[20];

void interrupt_handler(int sig);

/**
 * Utility
 */
__attribute__((noreturn))
void fatal(const char *msg) {
  perror(msg);
  exit(1);
}

void print(const char *msg) {
  write(STDOUT_FILENO, msg, strlen(msg));
}

void printval(const char *msg, size_t v) {
  char buf[24], *p;
  print(msg);
  p = buf + sizeof(buf);
  *--p = '\0';
  *--p = '\n';
  do {
    *--p = 0x30 + (v % 10);
    v /= 10;
  } while (v > 0);
  print(p);
}

size_t getlong(const char *msg) {
  char buf[24] = {};
  print(msg);
  read(STDIN_FILENO, buf, sizeof(buf) - 1);
  return atol(buf);
}

/**
 * Controller
 */
void io_set(off_t offset, void *data, size_t size) {
  lseek(mapfd, offset, SEEK_SET);
  write(mapfd, data, size);
}

void io_get(off_t offset, void *data, size_t size) {
  lseek(mapfd, offset, SEEK_SET);
  read(mapfd, data, size);
}

DEFINE_SETTER_CONST(int, command);
DEFINE_GETTER(int, command);
DEFINE_SETTER(ssize_t, index);
DEFINE_GETTER(ssize_t, index);
DEFINE_SETTER(size_t, value);
DEFINE_GETTER(size_t, value);

/**
 * Interface process: Human interface
 */
void note_interface(void) {
  while (1) {
    /* Server process done */
    print("1. edit\n"
          "2. show\n");

    switch (getlong("> ")) {
      case 1: { // edit
        ssize_t idx = getlong("index: ");
        size_t val = getlong("value: ");
        if (idx < 0 || idx >= ARR_SIZE) {
          print("[-] invalid index\n");
          break;
        }

        io_set_index(&idx);
        io_set_value(&val);
        io_set_command(CMD_EDIT);

        WAIT_RESPONSE();
        print("[+] ok\n");
        break;
      }

      case 2: { // show
        ssize_t idx = getlong("index: ");
        if (idx < 0 || idx >= ARR_SIZE) {
          print("[-] invalid index\n");
          break;
        }

        io_set_index(&idx);
        io_set_command(CMD_SHOW);

        WAIT_RESPONSE();
        printval("value: ", io_get_value());
        break;
      }

      default: { // exit
        print("[+] bye\n");
        io_set_command(CMD_EXIT);
        return;
      }
    }
  }
}

/**
 * Core process: Note manager
 */
void note_core(void) {
  size_t *arr = (size_t*)calloc(ARR_SIZE, sizeof(size_t));
  if (!arr) {
    if (verbose == 1)
      dprintf(STDERR_FILENO, "[DEBUG] Memory allocation failed\n");
    return;
  }

  while (1) {
    WAIT_REQUEST();

    /* Command sent from client */
    switch (io_get_command()) {
      case CMD_EDIT: {
        ssize_t idx = io_get_index();
        size_t val = io_get_value();
        arr[idx] = val;
        if (verbose == 1)
          dprintf(STDERR_FILENO, "[DEBUG] CMD_EDIT: %p <-- 0x%016lx\n", &arr[idx], val);
        break;
      }

      case CMD_SHOW: {
        ssize_t idx = io_get_index();
        io_set_value(&arr[idx]);
        if (verbose == 1)
          dprintf(STDERR_FILENO, "[DEBUG] CMD_SHOW: %p --> 0x%016lx\n", &arr[idx], arr[idx]);
        break;
      }

      default:
        if (verbose == 1)
          dprintf(STDERR_FILENO, "[DEBUG] CMD_EXIT\n");
        free(arr);
        return;
    }

    io_set_command(CMD_WAIT);
  }
}

/**
 * Entry point
 */
int main(int argc, char **argv, char **envp) {
  pid_t pid;

  /* Create filename */
  snprintf(mapname, sizeof(mapname), "/tmp/.shm-%08x", rand());

  /* Check verbose mode */
  if (argc > 2 && strcmp(argv[1], "-v") == 0)
    verbose = atoi(argv[2]);
  else
    verbose = atoi("0");

  if (verbose == 1)
    dprintf(STDERR_FILENO, "[DEBUG] Enabled verbose mode\n");

  /* Create shared memory */
  if ((mapfd = open(mapname, O_RDWR|O_CREAT|O_EXCL)) == -1)
    fatal(mapname);
  fchmod(mapfd, 0600);
  ftruncate(mapfd, sizeof(ArrayIO));
  signal(SIGINT, interrupt_handler);
  io_set_command(CMD_WAIT);

  if (verbose == 1)
    dprintf(STDERR_FILENO, "[DEBUG] Created shared memory at '%s'\n", mapname);

  /* Separate process */
  pid = fork();
  if (pid == -1) {
    fatal("fork");

  } else if (pid == 0) {
    /* Child process */
    if (verbose == 1)
      dprintf(STDERR_FILENO, "[DEBUG] interface: PID=%d\n", getpid());
    note_interface();

  } else {
    /* Parent process */
    if (verbose == 1)
      dprintf(STDERR_FILENO, "[DEBUG] core: PID=%d\n", getpid());
    note_core();
    wait(NULL);
  }

  return 0;
}

__attribute__((constructor))
void setup(void) {
  setreuid(geteuid(), geteuid());
  srand(time(NULL));
  alarm(300);
}

__attribute__((destructor))
void cleanup(void) {
  if (mapfd != -1) {
    close(mapfd);
    mapfd = -1;
    unlink(mapname);
  }
}

void interrupt_handler(int sig) {
  exit(0);
}
