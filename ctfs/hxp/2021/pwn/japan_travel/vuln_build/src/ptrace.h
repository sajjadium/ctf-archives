#pragma once

#include <sys/types.h>
#include <sys/user.h>
#include <stdbool.h>

enum stop_type {
	ST_EXITED,
	ST_SIGNALED,
	ST_STOPPED,
	ST_EVENT,
	ST_SYSCALL,
	ST_STILLALIVE
};

struct pt_stop {
	enum stop_type type;
	pid_t pid;
	union {
		struct {
			int exit_code;
		} exited;
		struct {
			int signal;
			bool dumped;
		} signaled;
		struct {
			int signal;
		} stopped;
		struct {
			int signal;
			int event;
		} event;
		struct user_regs_struct syscall_regs;
	};
};

pid_t start_trace(int (*pre)(void *), void *pre_args, int (*fun)(void *), void *args);

void pt_wait(pid_t pid, struct pt_stop *out, bool noblock);

ssize_t readvm(pid_t pid, void *local, void *remote, size_t len);

ssize_t readstr(pid_t pid, char **local, void *remote);

ssize_t writevm(pid_t pid, void *local, void *remote, size_t len);
