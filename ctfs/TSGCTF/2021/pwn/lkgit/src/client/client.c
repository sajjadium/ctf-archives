/******
 * 
 * lkgit: Git in Linux Kernel
 * 
 * This program is an example client program.
 * You can impl your own client as you like :)
 * It means that YOU CAN IGNORE THIS FILE,
 * though it may help you understand the module.
 * 
 * Note that the module is under development and has some limitations such as file size.
 * 
 * Example Usage:
 *  $ ./client snap hello.txt "initial commit"
 *  $ ./client log 300100003c012c0040007f0000784a3f
 *  $ ./client amend 300100003c012c0040007f0000784a3f "this is amended message"
 * 
******/

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>

#include "../include/lkgit.h"

#define ERR_DIE(msg) { printf("[ERROR] %s\n", msg); puts("\n[-] exiting..."); exit(1); }
#define UNIMPLEMENTED(cmd) { printf("[ERROR] unimplemented: %s\n", cmd); exit(1); }

#define DBNAME "/tmp/.lkgit.objects"

int lkgit_fd;

char* read_til_end(FILE *file) {
  unsigned n = 0;
  char *buf = malloc(0x10);
  while(fread(buf + n++, 1, 1, file) == 1) {
    if(n + 1 >= sizeof(buf)) {
      buf = realloc(buf, n * 2);
    }
  }
  return buf;
}

// convert hash bytes into printable string.
char* hash_to_string(char *hash) {
  char *hash_str = calloc(HASH_SIZE * 2 + 1, 1);
  for(int ix = 0; ix != HASH_SIZE; ++ix) {
    sprintf(hash_str + ix*2, "%02lx", (unsigned long)(unsigned char)hash[ix]);
  }
  return hash_str;
}

// convert string into bytes.
char *string_to_hash(char *hash_str) {
  char *hash = calloc(HASH_SIZE, 1);
  char buf[3] = {0};
  for(int ix = 0; ix != HASH_SIZE; ++ix) {
    memcpy(buf, &hash_str[ix*2], 2);
    hash[ix] = (char)strtol(buf, NULL, 16);
  }
  return hash;
}

// take a snapshot of a file.
char snap_file(char *filename, char *message) {
  FILE* file = fopen(filename, "rb");
  if(file == NULL) {
    printf("[ERROR] failed to open file: %s\n", filename);
    return -1;
  }

  char *content = read_til_end(file);
  hash_object req = {
      .content = content,
      .message = message,
  };
  if(ioctl(lkgit_fd, LKGIT_HASH_OBJECT, &req) != 0) {
    printf("[ERROR] failed to hash the object.\n");
  }

  FILE* db = fopen(DBNAME, "a");
  if(db < 0) {
    printf("[ERROR] failed to open database file: %s\n", DBNAME);
  }
  fprintf(db, "%s\n", hash_to_string(req.hash));
  puts(hash_to_string(req.hash));

  fclose(file);
  fclose(db);
  return 0;
}

// get a log of the given hash.
log_object* get_log_single(char *hash) {
  log_object *req = malloc(sizeof(log_object));
  memcpy(req->hash, hash, HASH_SIZE);
  if(ioctl(lkgit_fd, LKGIT_GET_OBJECT, req) != 0) {
    return NULL;
  } else {
    return req;
  }
}

// amend a commit message of the given hash.
log_object* amend_commit(char *hash, char *new_msg) {
  log_object *req = malloc(sizeof(log_object));
  memcpy(req->hash, hash, HASH_SIZE);
  memcpy(req->message, new_msg, MESSAGE_MAXSZ);
  if(ioctl(lkgit_fd, LKGIT_AMEND_MESSAGE, req) != 0) {
    return NULL;
  } else {
    return req;
  }
}

void usage(void) {
    puts("lkgit: Git in Linux Kernel");
    puts("Usage: ");
    puts("\tsnap <filename> <commit message>: take a snapshot of the file.");
    puts("\tcheckout <hash>: revert to a file at a point of given hash.");
    puts("\tamend <hash> <new message>: rewrite commit message.");
    puts("\tlog <hash>: see the commit.");
}

void print_log(log_object *log) {
  printf("HASH   : %s\n", hash_to_string(log->hash));
  printf("MESSAGE: %s\n", log->message);
  printf("CONTENT: \n%s\n", log->content);
}

int main(int argc, char *argv[])
{
  if (argc < 2) {
    usage();
    return 0;
  }

  lkgit_fd = open("/dev/lkgit", O_RDWR);
	if(lkgit_fd < 0) {
		ERR_DIE("open");
	}

  if (strcmp(argv[1], "snap") == 0) {
    if(argc != 4) usage();
    else          snap_file(argv[2], argv[3]);
  } else if(strcmp(argv[1], "log") == 0) {
    if(argc != 3) usage();
    else {
      log_object *log = get_log_single(string_to_hash(argv[2]));
      if(log == NULL) {
        printf("[ERROR] failed to fetch log: %s\n", argv[2]);
      } else {
        print_log(log);
      }
    }
  } else if(strcmp(argv[1], "amend") == 0)  {
    if(argc != 4) usage();
    else {
      log_object *log = amend_commit(string_to_hash(argv[2]), argv[3]);
      if(log == NULL) {
        printf("[ERROR] failed to amend commit message: %s\n", argv[2]);
      } else {
        puts("Here is OLD log: :");
        print_log(log);
      }
    }
  } else if(strcmp(argv[1], "checkout") == 0) {
    UNIMPLEMENTED(argv[1]);
  } else {
    printf("unknown command: %s\n", argv[1]);
  }

  return 0;
}
