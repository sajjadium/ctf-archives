// SPDX-License-Identifier: Apache-2.0
/*
 * Copyright 2021 Google LLC.
 */

#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/inotify.h>
#include <sys/stat.h>
#include <unistd.h>

#define min(a, b) ((a) < (b) ? (a) : (b))

static int uploads_fd;
static int req_dir_top_fd;
static int inotify_fd;

static void perror_exit(char *msg)
{
	perror(msg);
	exit(1);
}

static void *handle_request(void *arg)
{
	int res_errno;
	int req_dir;
	char *name = arg;
	int req_id_fd = -1;
	struct stat req_id_stat;
	size_t req_id_size;
	char *id_buf = NULL;
	ssize_t n_read;
	int in_fd = -1;
	int out_fd = -1;
	struct stat data_stat;
	size_t data_size;
	FILE *out_errno_file;

	if ((req_dir = openat(req_dir_top_fd, name, O_PATH | O_CLOEXEC)) < 0)
		goto out;

	// Because guest might die, we can't be patient forever. Do 5 seconds.
	for (int i = 0; i < 500; i++) {
		if (!faccessat(req_dir, "id_complete", F_OK, 0))
			break;

		usleep(10000);
	}

	if (faccessat(req_dir, "id_complete", F_OK, 0))
		goto out;

	if ((req_id_fd = openat(req_dir, "id", O_RDONLY | O_CLOEXEC)) < 0)
		goto out_write_errno;

	if (fstat(req_id_fd, &req_id_stat))
		goto out_write_errno;
	req_id_size = req_id_stat.st_size;

	if (!(id_buf = calloc(req_id_size + 1, 1)))
		goto out_write_errno;

	n_read = read(req_id_fd, id_buf, req_id_size);
	if (n_read < 0)
		goto out_write_errno;
	if (n_read != req_id_size) {
		// the request is long enough that we can't read in one syscall
		errno = EOVERFLOW;
		goto out_write_errno;
	}

	for (size_t i = 0; i < req_id_size; i++) {
		if (id_buf[i] >= 'a' && id_buf[i] <= 'z')
			continue;
		if (id_buf[i] >= 'A' && id_buf[i] <= 'Z')
			continue;
		if (id_buf[i] >= '0' && id_buf[i] <= '9')
			continue;

		errno = EINVAL;
		goto out_write_errno;
	}

	if ((in_fd = openat(uploads_fd, id_buf, O_RDONLY | O_CLOEXEC)) < 0)
		goto out_write_errno;

	if ((out_fd = openat(req_dir, "data",
			O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0644)) < 0)
		goto out_write_errno;

	if (fstat(in_fd, &data_stat))
		goto out_write_errno;
	data_size = data_stat.st_size;

	// Actually do the copy from in_fd to out_fd
	while (data_size) {
		char buf[1048576];
		char *c_buf = buf;
		ssize_t n_read = read(in_fd, buf, min(data_size, sizeof(buf)));

		if (n_read < 0)
			goto out_write_errno;

		data_size -= n_read;

		while (n_read) {
			ssize_t n_write = write(out_fd, c_buf, n_read);

			if (n_write < 0)
				goto out_write_errno;

			n_read -= n_write;
			c_buf += n_write;
		}
	}

	fdatasync(out_fd);

	goto out_complete;

out_write_errno:
	res_errno = errno;

	close(out_fd);
	if ((out_fd = openat(req_dir, "errno",
			O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0644)) < 0)
		goto out;
	if (!(out_errno_file = fdopen(out_fd, "w")))
		goto out;

	fprintf(out_errno_file, "%d", res_errno);
	fclose(out_errno_file);
	out_fd = -1;

out_complete:
	close(out_fd);
	if ((out_fd = openat(req_dir, "complete",
			O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0644)) < 0)
		goto out;

out:
	free(id_buf);
	free(name);
	close(req_id_fd);
	close(in_fd);
	close(out_fd);
	return NULL;
}

int main(int argc, char *argv[])
{
	if ((uploads_fd = open("/tmp/uiuctf-uploads", O_PATH | O_CLOEXEC)) < 0)
		perror_exit("openat");

	if ((req_dir_top_fd = open("/tmp/uiuctf-comm", O_PATH | O_CLOEXEC)) < 0)
		perror_exit("openat");

	inotify_fd = inotify_init1(IN_CLOEXEC);
	if (inotify_fd < 0)
		perror_exit("inotify_init1");

	if (inotify_add_watch(inotify_fd, "/tmp/uiuctf-comm", IN_CREATE | IN_ONLYDIR) < 0)
		perror_exit("inotify_add_watch");

	while (true) {
		char buf[10 * (sizeof(struct inotify_event) + NAME_MAX + 1)] __attribute__ ((aligned(8)));
		ssize_t len = read(inotify_fd, buf, sizeof(buf));

		if (len < 0)
			perror_exit("read(inotify)");

		for (char *p = buf; p < buf + len;) {
			struct inotify_event *event = (void *)p;
			char *name;
			pthread_attr_t thread_attr;
			pthread_t thread;

			if (event->mask != (IN_CREATE | IN_ISDIR))
				continue;
			if (!event->len)
				continue;

			name = strdup(event->name);
			if (!name)
				perror_exit("strdup");

			// musl default stack stice is not enough to hold 1MB
			// which we use to do the file copy
			if (pthread_attr_init(&thread_attr))
				perror_exit("pthread_attr_init");
			if (pthread_attr_setstacksize(&thread_attr, 1048576 * 2))
				perror_exit("pthread_attr_setstacksize");

			// The reason a thread is started to process immediately
			// instead of adding directory to inotify is because of
			// races -- after adding to inotify it needs to check
			// the existance anyways to account for any missed inotify
			// events. If it exists it would then need to cancel the
			// inotify watch, but then what if inotify did receive
			// the event? This is too many races to think about and
			// reason.

			if (pthread_create(&thread, &thread_attr, handle_request, name))
				perror_exit("pthread_create");
			if (pthread_detach(thread))
				perror_exit("pthread_detach");

			if (pthread_attr_destroy(&thread_attr))
				perror_exit("pthread_attr_destroy");

			p += sizeof(struct inotify_event) + event->len;
		}
	}
}
