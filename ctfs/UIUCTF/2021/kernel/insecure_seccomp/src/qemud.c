// SPDX-License-Identifier: Apache-2.0
/*
 * Copyright 2021 Google LLC.
 */

#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <poll.h>
#include <pthread.h>
#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

// Why is this here? Because qemu doesn't auto terminate on EOF.
// If stdin die then qemu must die.

static pid_t qemu_pid;
static bool qemu_alive;

static int stdin_pipe[2];
static char *bzImage;

static void perror_exit(char *msg)
{
	perror(msg);
	exit(1);
}

static void wait_pid_terminate(pid_t pid)
{
	while (true) {
		int wstatus;
		pid_t w = waitpid(pid, &wstatus, WUNTRACED | WCONTINUED);

		if (w < 0) {
			if (errno == ERESTART || errno == EINTR)
				continue;
			perror_exit("waitpid");
		}

		if (WIFEXITED(wstatus) || WIFSIGNALED(wstatus))
		 	break;
	}
}

static void *stdin_thread_fn(void *arg)
{
	struct pollfd pollfd = {
		.fd = STDIN_FILENO,
		.events = POLLIN,
	};

	while (true) {
		if (poll(&pollfd, 1, -1) < 0) {
			if (errno == ERESTART || errno == EINTR)
				continue;
			perror_exit("poll");
		}

		char buf[4096];
		char *c_buf = buf;
		ssize_t n_read = read(STDIN_FILENO, buf, sizeof(buf));

		if (n_read < 0)
			perror_exit("read");
		if (!n_read)
			exit(0);

		while (n_read) {
			ssize_t n_write = write(stdin_pipe[1], c_buf, n_read);

			if (n_write < 0)
				perror_exit("write");

			n_read -= n_write;
			c_buf += n_write;
		}
	}
}

static void kill_qemu(void)
{
	if (qemu_alive)
		kill(qemu_alive, SIGTERM);
}

int main(int argc, char *argv[])
{
	if (argc < 2) {
		fprintf(stderr, "Usage: %s [bzImage]\n", argv[0]);
		exit(1);
	}

	bzImage = argv[1];

	if (pipe2(stdin_pipe, O_CLOEXEC))
		perror_exit("pipe2");

	qemu_pid = fork();
	if (qemu_pid < 0)
		perror_exit("fork");

	if (qemu_pid) {
		pthread_t stdin_thread;

		if (pthread_create(&stdin_thread, NULL, stdin_thread_fn, NULL))
			perror_exit("pthread_create");

		wait_pid_terminate(qemu_pid);
		qemu_alive = false;

		exit(0);
	} else {
		if (dup2(stdin_pipe[0], STDIN_FILENO))
			perror_exit("dup2");

		qemu_alive = true;
		atexit(kill_qemu);

		execl("/usr/bin/qemu-system-x86_64", "qemu-system-x86_64",
			"-no-reboot",
			"-cpu", "max",
			"-m", "64M",
			"-display", "none",
			"-monitor", "none",
			"-serial", "stdio",
			"-kernel", bzImage,
			NULL);

		perror_exit("execl");
	}

	return 0;
}
