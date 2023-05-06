#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>

#define RESPONSE(x)                                       \
  {                                                       \
    res = x;                                              \
    if (write(p2c, &res, sizeof(res)) != sizeof(res))     \
      exit(0);                                            \
  }
#define WAIT()                                         \
  {                                                    \
    if (read(p2c, &res, sizeof(res)) != sizeof(res))   \
      exit(1);                                         \
  }

enum Command {NEW, SET, GET};

typedef struct {
  enum Command cmd;
  union {
    size_t size;
    off_t index;
  };
  uint64_t value;
} request_t;

/**
 * Utilities
 */
void print(const char *msg) {
  if (write(1, msg, strlen(msg)) < 0)
    exit(1);
}

void printlong(uint64_t v) {
  char buf[32], *ptr = &buf[31];
  *ptr = '\0';
  if (v) {
    while (v) {
      *--ptr = '0'+(v%10);
      v /= 10;
    }
  } else {
    *--ptr = '0';
  }
  print(ptr);
}

long getlong(const char *msg) {
  char buf[32];
  print(msg);
  if (read(0, buf, 322) < 0)
    exit(1);
  return atol(buf);
}

/**
 * Child process (interface)
 */
void child_note(int c2p, int p2c, int ppid) {
  int res;
  request_t req;
  uint64_t value;

  print("1. new\n");
  print("2. set\n");
  print("3. get\n");

  while (1) {
    long choice = getlong("> ");

    switch (choice)
    {
      /* New */
      case 1: {
        long size = getlong("size: ");

        /* Send request */
        req.cmd = NEW;
        req.size = size;
        if (write(c2p, &req, sizeof(req)) != sizeof(req))
          exit(1);

        /* Check result */
        WAIT();
        if (res == 0)
          print("[+] success\n");
        else
          print("[-] failed\n");
        break;
      }

      /* Set */
      case 2: {
        long index = getlong("index: ");
        long value = getlong("value: ");

        /* Send request */
        req.cmd = SET;
        req.index = index;
        req.value = value;
        if (write(c2p, &req, sizeof(req)) != sizeof(req))
          exit(1);
        
        /* Check result */
        WAIT();
        if (res == 0)
          print("[+] success\n");
        else
          print("[-] failed\n");
        break;
      }

      /* Get */
      case 3: {
        long index = getlong("index: ");

        /* Send request */
        req.cmd = GET;
        req.index = index;
        if (write(c2p, &req, sizeof(req)) != sizeof(req))
          exit(1);

        /* Check result */
        WAIT();
        if (res != 0) {
          print("[-] failed\n");
          break;
        }

        if (read(p2c, &value, sizeof(uint64_t)) != sizeof(uint64_t))
          exit(1);

        /* Show value */
        print("array[");
        printlong(req.index);
        print("] = ");
        printlong(value);
        print("\n[+] success\n");
        break;
      }

    default:
      return;
    }
  }
}

/**
 * Parent process (core)
 */
void parent_note(int c2p, int p2c, int cpid) {
  int res;
  request_t req;

  uint64_t *old, *buffer = (uint64_t*)malloc(0);
  size_t size = 0;

  while (1) {
    if (read(c2p, &req, sizeof(req)) != sizeof(req))
      return;

    switch (req.cmd)
    {
      /* Create new buffer */
      case NEW: {
        if (req.size > 2800) {
          /* Invalid size*/
          RESPONSE(-1);
          break;
        }

        /* Allocate new buffer */
        old = buffer;
        if (!(buffer = (uint64_t*)malloc(req.size * sizeof(uint64_t)))) {
          /* Memory error */
          size = -1;
          RESPONSE(-1);
          break;
        }

        /* Prevent memory leak */
        free(old);

        /* Update size */
        size = req.size;

        RESPONSE(0);
        break;
      }

      /* Set value */
      case SET: {
        if (req.index < 0 || req.index >= size) {
          /* Invalid index */
          RESPONSE(-1);
          break;
        }

        /* Set value */
        buffer[req.index] = req.value;

        RESPONSE(0);
        break;
      }

      /* Get value */
      case GET: {
        if (req.index < 0 || req.index >= size) {
          /* Invalid index */
          RESPONSE(-1);
          break;
        }
        RESPONSE(0);

        /* Send value */
        write(p2c, &buffer[req.index], sizeof(uint64_t));
        break;
      }

      default:
        free(buffer);
        return;
    }
  }
}

void setup_sandbox() {
  static unsigned char filter[] = {
    32,0,0,0,4,0,0,0,21,0,0,17,62,0,0,192,32,0,0,0,0,0,0,0,
    53,0,15,0,0,0,0,64,21,0,14,0,2,0,0,0,21,0,13,0,1,1,0,0,
    21,0,12,0,59,0,0,0,21,0,11,0,66,1,0,0,21,0,10,0,85,0,0,
    0,21,0,9,0,57,0,0,0,21,0,8,0,58,0,0,0,21,0,7,0,56,0,0,0,
    21,0,6,0,101,0,0,0,21,0,5,0,62,0,0,0,21,0,4,0,200,0,0,0,
    21,0,3,0,234,0,0,0,21,0,2,0,54,1,0,0,21,0,1,0,55,1,0,0,
    6,0,0,0,0,0,255,127,6,0,0,0,0,0,0,0
  };
  struct prog {
    unsigned short len;
    unsigned char *filter;
  } rule = {
    .len = sizeof(filter) >> 3,
    .filter = filter
  };

  if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) {
    perror("prctl(PR_SET_NO_NEW_PRIVS)");
    exit(1);
  }
  if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &rule) < 0) {
    perror("prctl(PR_SET_SECCOMP)");
    exit(1);
  }
}

int main() {
  int cpid, ppid, c2p[2], p2c[2];

  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  ppid = getpid();

  if (pipe(c2p) == -1 || pipe(p2c) == -1) {
    perror("pipe");
    return 1;
  }

  if ((cpid = fork()) == -1) {
    perror("fork");
    return 1;
  }

  if (cpid == 0) {

    /* Child process: sandboxed */
    close(c2p[0]);
    close(p2c[1]);
    setup_sandbox();
    child_note(c2p[1], p2c[0], ppid);

  } else {

    /* Parent process: unsandboxed */
    close(c2p[1]);
    close(p2c[0]);
    parent_note(c2p[0], p2c[1], cpid);
    wait(NULL);

  }

  return 0;
}
