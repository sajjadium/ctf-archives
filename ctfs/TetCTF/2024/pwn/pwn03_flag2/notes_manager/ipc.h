/*
 * Simple Linux IPC backed by share memory and eventfd
 * Author: peternguyen93
 */

#ifndef IPC_H
#define IPC_H
#include <stdint.h>
#include <stddef.h>
#include <errno.h>
#include <sys/eventfd.h>

#define SHM_MEM_PATH "shm_mem.emu"
#define SHM_MEM_MAX_SIZE 0x10000
#define SHM_EVFD_ENV "EVFD"

struct IPC {
	int evfd_sender;
	int evfd_receiver;
	//int pipe_read;
	//int pipe_write;
	int shm_fd;
	void *shm_addr;
	size_t shm_size;
};

//extern struct IPC ipc;
typedef struct IPC * IPC_t;
void IPC_create(IPC_t ipc, int create_ev_fd, int ev_flags, int create_shm);
void IPC_detroy(IPC_t ipc, int close_ev_fd);

typedef enum msg_type {
	SENDER = 0,
	RECEIVER = 1
} msg_type_t;

int send_data(IPC_t ipc, msg_type_t msg_type, const void *data, uint64_t data_size);
int recv_data(IPC_t ipc, msg_type_t msg_type, void**out_data, uint64_t *out_size);
int recv_data_timeout(IPC_t ipc, msg_type_t msg_type, void**out_data, uint64_t *out_size, uint32_t timeout);

void serialize_ev_fd(IPC_t ipc, char *buf, size_t buf_size);
void parse_ev_fds(IPC_t ipc, char *fds_str);

#define IS_OK(rc) (rc == sizeof(uint64_t))
#define IS_TIMEOUT(rc) (rc == EAGAIN)
#define IS_ERR(rc) (rc < 0)

#endif
