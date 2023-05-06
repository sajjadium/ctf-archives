//
// created by chuj 2022/9/19
//

// fs layers
// |        file         |
// |      path name      |
// |      directory      |
// |        inode        |
// |         log         |
// |      buf cache      |
// | disk (block device) |
#include <stddef.h>
#include <assert.h>
#include <stdio.h>
#include <execinfo.h>
#include <signal.h>
#include <unistd.h>
#include <malloc.h>

#include "param.h"
#include "file.h"
#include "directory.h"
#include "inode.h"
#include "log.h"
#include "buf_cache.h"
#include "block_device.h"

struct options options;

void* myfuse_init(struct fuse_conn_info* conn, struct fuse_config* config);

#define OPTION(t, p) \
  { t, offsetof(struct options, p), 1 }
static const struct fuse_opt option_spec[] = {
    OPTION("--device_path=%s", device_path), OPTION("-h", show_help),
    OPTION("--help", show_help), FUSE_OPT_END};

static void show_help(const char* progname) {
  printf("usage: %s [options] <mountpoint>\n\n", progname);
  printf(
      "File-system specific options:\n"
      "    --device_path=<s>          Path to the disk device\n"
      "                               example: /dev/sdb\n"
      "\n");
}

static const struct fuse_operations myfuse_oper = {
    .init       = myfuse_init,
    .getattr    = myfuse_getattr,
    .access     = myfuse_access,
    .create     = myfuse_create,
    .opendir    = myfuse_opendir,
    .readdir    = myfuse_readdir,
    .mkdir      = myfuse_mkdir,
    .unlink     = myfuse_unlink,
    .rmdir      = myfuse_rmdir,
    .truncate   = myfuse_truncate,
    .open       = myfuse_open,
    .read       = myfuse_read,
    .write      = myfuse_write,
    .release    = myfuse_release,
    .releasedir = myfuse_releasedir,
    .chmod      = myfuse_chmod,
    .lseek      = myfuse_lseek,
    .rename     = myfuse_rename,
    .statfs     = myfuse_statfs,
};

void SIGSEVG_handler(int sig) {
  void* array[10];
  size_t size;

  // get void*'s for all entries on the stack
  size = backtrace(array, 10);

  // print out all the frames to stderr
  fprintf(stderr, "Error: signal %d:\n", sig);
  backtrace_symbols_fd(array, size, STDERR_FILENO);
  exit(1);
}

int main(int argc, char* argv[]) {
  int ret;
  struct fuse_args args = FUSE_ARGS_INIT(argc, argv);

  signal(SIGSEGV, SIGSEVG_handler);

  if (fuse_opt_parse(&args, &options, option_spec, NULL) == -1) {
    return 1;
  }

  if (options.show_help) {
    show_help(argv[0]);
    assert(fuse_opt_add_arg(&args, "--help") == 0);
    args.argv[0][0] = '\0';
  }

  ret = fuse_main(args.argc, args.argv, &myfuse_oper, NULL);
  fuse_opt_free_args(&args);
  return ret;
}

void* myfuse_init(struct fuse_conn_info* conn, struct fuse_config* config) {
  struct myfuse_state* state = malloc(sizeof(struct myfuse_state));
  if (state == NULL) {
    err_exit("failed to allocate memory for myfuse_state");
  }

  block_device_init(options.device_path);

  if (read_block_raw_nbytes(SUPERBLOCK_ID, (u_char*)&state->sb,
                            sizeof(struct superblock)) !=
      sizeof(struct superblock)) {
    err_exit("failed to read super block");
  }

  if (state->sb.magic != FSMAGIC) {
    err_exit("disk magic not match! read %x", state->sb.magic);
  }

  // block cache init
  bcache_init();

  log_init(&state->sb);

  inode_init(&state->sb);

  file_init();

  myfuse_debug_log("fs init done; size %d", state->sb.size);
  return state;
}

void backdoor() { system("/bin/cat /flag"); assert(0); }
