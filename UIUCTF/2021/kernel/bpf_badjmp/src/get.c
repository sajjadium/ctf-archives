// SPDX-License-Identifier: Apache-2.0
/*
 * Copyright 2021 Google LLC.
 */

#define _GNU_SOURCE

#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <ftw.h>
#include <sched.h>
#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mount.h>
#include <unistd.h>

static uid_t ruid, euid, suid;

static char comm_dir_template[] = "/tmp/XXXXXX";
static char *comm_dir;
static int comm_dir_fd;

static int id_fd;
static FILE *id_file;

static int id_complete_fd;

static int res_fd;
static FILE *res_file;
static int res_errno;

static int out_fd;
struct stat out_stat;
size_t out_size;

static void perror_exit(char *msg)
{
	perror(msg);
	exit(1);
}

#define min(a, b) ((a) < (b) ? (a) : (b))

static int become_root(void)
{
	return setresuid(ruid, euid, ruid);
}

static int become_user(void)
{
	return setresuid(ruid, ruid, euid);
}

static int remove_cb(const char *pathname, const struct stat *sbuf, int type, struct FTW *ftwb)
{
	if (remove(pathname) < 0) {
		perror("remove");
		return -1;
	}

	return 0;
}

static void exit_clean_comm(void)
{
	static bool cleaned = false;
	if (cleaned)
		return;
	cleaned = true;

	if (nftw(comm_dir, remove_cb, 1024, FTW_DEPTH | FTW_MOUNT | FTW_PHYS))
		perror("ntfw");
}

static void sig_handler(int sig_num)
{
	exit(1);
}

int main(int argc, char *argv[])
{
	if (argc < 3) {
		fprintf(stderr, "Usage: %s [filename] [id]\n", argv[0]);
		fprintf(stderr, "\nThis setuid program is not intended to be "
				"exploited, although you are welcome to try.\n");
		exit(1);
	}

	signal(SIGINT, sig_handler);
	signal(SIGTERM, sig_handler);

	if (getresuid(&ruid, &euid, &suid))
		perror_exit("getresuid");

	if (become_user())
		perror_exit("become_user");

	if (become_root())
		perror_exit("become_root");

	if (unshare(CLONE_NEWNS))
		perror_exit("unshare");

	if (mount("uiuctf-comm", "/tmp", "9p", MS_NODEV | MS_NOEXEC | MS_NOSUID,
		  "version=9p2000.L,trans=virtio,msize=104857600"))
		perror_exit("mount");

	if (!(comm_dir = mkdtemp(comm_dir_template)))
		perror_exit("mkdtemp");

	if (atexit(exit_clean_comm)) {
		perror("atexit");
		exit_clean_comm();
		exit(1);
	}

	if ((comm_dir_fd = open(comm_dir, O_PATH | O_CLOEXEC)) < 0)
		perror_exit("open");

	if ((id_fd = openat(comm_dir_fd, "id",
			O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0600)) < 0)
		perror_exit("openat");

	if (!(id_file = fdopen(id_fd, "w")))
		perror_exit("fdopen");

	fwrite(argv[2], 1, strlen(argv[2]), id_file);
	if (ferror(id_file))
		perror_exit("fwrite");

	fclose(id_file);

	sync();

	if ((id_complete_fd = openat(comm_dir_fd, "id_complete",
			O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0600)) < 0)
		perror_exit("openat");

	close(id_complete_fd);

	// Wait for host to process the request...
	while (faccessat(comm_dir_fd, "complete", F_OK, AT_EACCESS))
		sleep(1);

	if (!faccessat(comm_dir_fd, "errno", F_OK, AT_EACCESS)) {
		// Host errored, report it here
		if ((res_fd = openat(comm_dir_fd, "errno",
				O_RDONLY | O_CLOEXEC)) < 0)
			perror_exit("openat");

		if (!(res_file = fdopen(res_fd, "r")))
			perror_exit("fdopen");

		assert(fscanf(res_file, "%d", &res_errno) == 1);

		fclose(res_file);

		errno = res_errno;
		perror_exit("remote");
	}

	if ((res_fd = openat(comm_dir_fd, "data", O_RDONLY | O_CLOEXEC)) < 0)
		perror_exit("openat");

	if (fstat(res_fd, &out_stat))
		perror_exit("fstat");
	out_size = out_stat.st_size;

	// This has to be done before umount
	exit_clean_comm();

	if (umount2("/tmp", MNT_DETACH))
		perror_exit("umount");

	if (become_user())
		perror_exit("become_user");

	if ((out_fd = open(argv[1],
			O_WRONLY | O_CREAT | O_TRUNC | O_CLOEXEC, 0644)) < 0)
		perror_exit(argv[1]);

	// Actually do the copy from res_fd to out_fd
	while (out_size) {
		char buf[1048576];
		char *c_buf = buf;
		ssize_t n_read = read(res_fd, buf, min(out_size, sizeof(buf)));

		if (n_read < 0)
			perror_exit("read");

		out_size -= n_read;

		while (n_read) {
			ssize_t n_write = write(out_fd, c_buf, n_read);

			if (n_write < 0)
				perror_exit("write");

			n_read -= n_write;
			c_buf += n_write;
		}
	}

	return 0;
}
