// SPDX-License-Identifier: Apache-2.0
/*
 * Copyright 2021 Google LLC.
 */

#define _GNU_SOURCE

#include <assert.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <poll.h>
#include <pthread.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/random.h>
#include <sys/socket.h>
#include <unistd.h>

#define container_of(ptr, type, member)					\
	__extension__							\
	({								\
		const __typeof__(((type *) NULL)->member) * __ptr = (ptr); \
		(type *)((char *)__ptr - offsetof(type, member));	\
	})

// list source: <urcu/list.h>
struct list_head {
	struct list_head *next, *prev;
};

#define LIST_HEAD(name) \
	struct list_head name ={ &(name), &(name) }

static inline
void list_add(struct list_head *newp, struct list_head *head)
{
	head->next->prev = newp;
	newp->next = head->next;
	newp->prev = head;
	head->next = newp;
}

static inline
void __list_del(struct list_head *prev, struct list_head *next)
{
	next->prev = prev;
	prev->next = next;
}

/* Remove element from list. */
static inline
void list_del(struct list_head *elem)
{
	__list_del(elem->prev, elem->next);
}

#define list_entry(ptr, type, member) 	container_of(ptr, type, member)

#define list_for_each_entry_safe(pos, p, head, member) \
	for (pos = list_entry((head)->next, __typeof__(*(pos)), member), \
			p = list_entry((pos)->member.next, __typeof__(*(pos)), member); \
		&(pos)->member != (head); \
		pos = (p), p = list_entry((pos)->member.next, __typeof__(*(pos)), member))


static pthread_t expirier_thread;
static int expirier_sktpair[2];

struct expirier_entry {
	struct list_head list;
	time_t expiry;
	char *path;
};

struct handle_struct {
	pthread_t thread;
	int connfd;
};

static void perror_exit(char *msg)
{
	perror(msg);
	exit(1);
}

static void *expirier_thread_fn(void *arg)
{
	struct pollfd pollfd = {
		.fd = expirier_sktpair[1],
		.events = POLLIN,
	};
	LIST_HEAD(files);

	while (true) {
		struct expirier_entry *exp, *tmp;
		int shortest_timeout = -1;
		int pollres;

		list_for_each_entry_safe(exp, tmp, &files, list) {
			ssize_t timeout = exp->expiry - time(NULL);

			if (timeout <= 0) {
				unlink(exp->path);
				free(exp->path);
				list_del(&exp->list);
				free(exp);
				continue;
			}

			if (shortest_timeout < 0 || timeout < shortest_timeout)
				shortest_timeout = timeout;
		}

		pollres = poll(&pollfd, 1, shortest_timeout * 1000);
		if (pollres < 0) {
			if (errno == ERESTART || errno == EINTR)
				continue;
			perror_exit("poll");
		}

		if (pollres) {
			ssize_t len = recv(expirier_sktpair[1], NULL, 0, MSG_PEEK | MSG_TRUNC);
			char *path;

			if (len < 0)
				perror_exit("recv");
			assert(len);

			path = calloc(len + 1, 1);
			assert(recv(expirier_sktpair[1], path, len, 0) == len);

			exp = malloc(sizeof(*exp));
			if (!exp)
				perror_exit("malloc");

			*exp = (typeof(*exp)) {
				.expiry = time(NULL) + 5 * 60,
				.path = path,
			};

			list_add(&exp->list, &files);
		}
	}

	return NULL;
}


static void *handle_request(void *arg)
{
	struct handle_struct *handle = arg;
	int file_fd = -1;

	while (true) {
		char buf[65536];
		char *c_buf = buf;
		ssize_t n_read = read(handle->connfd, buf, sizeof(buf));

		if (n_read < 0) {
			if (errno != ECONNRESET)
				perror("read");
			goto out;
		}
		if (!n_read)
			goto out;

		// We don't do this in the beginning because there is no need
		// to save an empty file.
		if (file_fd < 0) {
			char path[] = "/tmp/uiuctf-uploads/XXXXXXXX";
			char *msg;

			// We don't use mkstemp because the name is based off of time,
			// which is more predictable than urandom.
			for (int attempt = 0; attempt < 100; attempt++) {
				for (int i = 0; i < 8; i++) {
					char c;

					while (true) {
						if (getrandom(&c, 1, 0) != 1)
							perror_exit("getrandom");

						if (c >= 'a' && c <= 'z')
							break;
						if (c >= 'A' && c <= 'Z')
							break;
						if (c >= '0' && c <= '9')
							break;
					}

					path[20 + i] = c;
				}

				file_fd = open(path, O_RDWR | O_CREAT | O_EXCL, 0600);
				if (file_fd >= 0)
					break;

				if (errno != EEXIST)
					perror_exit("open");
			}

			if (file_fd < 0)
				perror_exit("max attempts exceeded creating upload file");

			if (asprintf(&msg,
				     "File id: %s\nYou may download the file "
				     "onto the VM by $ get [filename] %s\n"
				     "nc will exit when upload is complete.\n"
				     "File expires after 5 minutes. Max size: 32MiB\n",
				     path + 20,
				     path + 20) < 0)
				perror_exit("asprintf");

			(void)!write(handle->connfd, msg, strlen(msg));
			free(msg);

			shutdown(handle->connfd, SHUT_WR);

			send(expirier_sktpair[0], path, sizeof(path), 0);
		}

		while (n_read) {
			ssize_t n_write = write(file_fd, c_buf, n_read);

			if (n_write < 0) {
				if (errno != EFBIG)
					perror("write");
				goto out;
			}

			n_read -= n_write;
			c_buf += n_write;
		}
	}

out:
	close(file_fd);
	close(handle->connfd);
	free(handle);
	return NULL;
}

int main(int argc, char *argv[])
{
	int sockfd;
	struct sockaddr_in servaddr;

	if (socketpair(AF_UNIX, SOCK_DGRAM, 0, expirier_sktpair) < 0)
		perror_exit("socketpair");

	if (pthread_create(&expirier_thread, NULL, expirier_thread_fn, NULL))
		perror_exit("pthread_create");

	if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
		perror_exit("socket");

	servaddr = (struct sockaddr_in) {
		.sin_family = AF_INET,
		.sin_addr = { htonl(INADDR_ANY) },
		.sin_port = htons(1338),
	};

	if (bind(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)))
		perror_exit("bind");

	if (listen(sockfd, 5))
		perror_exit("listen");

	while (true) {
		struct sockaddr_in cliaddr;
		socklen_t len = sizeof(cliaddr);
		struct handle_struct *handle;
		int connfd;

		if ((connfd = accept(sockfd, (struct sockaddr *)&cliaddr, &len)) < 0)
			perror_exit("accept");

		handle = malloc(sizeof(*handle));
		if (!handle)
			perror_exit("malloc");
		handle->connfd = connfd;

		if (pthread_create(&handle->thread, NULL, handle_request, handle))
			perror_exit("pthread_create");
		if (pthread_detach(handle->thread))
			perror_exit("pthread_detach");
	}
}
