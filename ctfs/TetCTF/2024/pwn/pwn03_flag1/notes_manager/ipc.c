/*
 * Simple Linux IPC backed by share memory and eventfd
 * Author: peternguyen93
 */
#include "ipc.h"
#include <stdint.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/eventfd.h>
#include <sys/select.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include "dbg.h"

void IPC_create(IPC_t ipc, int create_ev_fd, int ev_flags, int create_shm)
{
	int event_fd;
	int oflags;

	if(create_ev_fd){
		event_fd = eventfd(0, ev_flags);
		assert_fail_f(event_fd > -1, "Unable to create eventfd for sender\n");
		ipc->evfd_sender = event_fd;

		event_fd = eventfd(0, ev_flags);
		assert_fail_f(event_fd > -1, "Unable to create eventfd for receiver\n");
		ipc->evfd_receiver = event_fd;
	}

	oflags = O_RDWR;
	if(create_shm){
		oflags |= O_CREAT;
	}
	ipc->shm_fd = shm_open(SHM_MEM_PATH, oflags, 0666);
	assert_fail_f(ipc->shm_fd > -1, "Unable to create shm_fd\n");

	assert_fail_f(ftruncate(ipc->shm_fd, SHM_MEM_MAX_SIZE) != -1, "Unable to ftruncate share memory\n");

	void *share_addr = mmap(NULL, SHM_MEM_MAX_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, ipc->shm_fd, 0);
	assert_fail_f(share_addr != (void *)-1, "Unable to map shared memory\n");
	ipc->shm_addr = share_addr;
}

int send_data(IPC_t ipc, msg_type_t msg_type, const void *data, uint64_t data_size)
{
	uint64_t use_count = data_size;
	int evfd = msg_type == RECEIVER ? ipc->evfd_receiver : ipc->evfd_sender;
	int rc;

	assert_fail_f(data_size > 0, "data_size must not be NULL\n");
	rc = write(evfd, &use_count, sizeof(uint64_t));
	if(rc == sizeof(uint64_t) && data){
		assert_fail_f(sizeof(data_size) + data_size <= SHM_MEM_MAX_SIZE, "Message too big\n");
		memcpy(ipc->shm_addr, data, data_size);
	}

	return rc;
}

int recv_data_timeout(
		IPC_t ipc,
		msg_type_t msg_type,
		void **out_data,
		uint64_t *out_size,
		uint32_t timeout)
{
	int evfd = msg_type == RECEIVER ? ipc->evfd_receiver : ipc->evfd_sender;
	int rc = -1;
	uint64_t use_count = 0;
	uint32_t tmp_timeout = 1;

	assert_fail_f(out_size, "out_size must not be NULL\n");

	if(timeout) {
		tmp_timeout = timeout;
		while(tmp_timeout--){
			rc = read(evfd, &use_count, sizeof(uint64_t));
			//DBG("rc = %d\n", rc);
			if(IS_OK(rc)){
				break;
			}
			sleep(1);
		};
	} else {
		rc = read(evfd, &use_count, sizeof(uint64_t));
	}

	if(IS_OK(rc)){
		*out_size = use_count;
		if(out_data){
			*out_data = ipc->shm_addr;
		}
	} else if(!tmp_timeout){
		rc = EAGAIN;
	}

	return rc;
}

int recv_data(
		IPC_t ipc,
		msg_type_t msg_type,
		void **out_data,
		uint64_t *out_size)
{
	return recv_data_timeout(ipc, msg_type, out_data, out_size, 0);
}

void IPC_detroy(IPC_t ipc, int close_ev_fd)
{
	if(close_ev_fd){
		close(ipc->evfd_receiver);
		close(ipc->evfd_sender);
	}

	munmap(ipc->shm_addr, SHM_MEM_MAX_SIZE);
	close(ipc->shm_fd);
	bzero((void *)ipc, sizeof(struct IPC));
}

void serialize_ev_fd(IPC_t ipc, char *buf, size_t buf_size)
{
	snprintf(buf, buf_size, "%d-%d", ipc->evfd_receiver, ipc->evfd_sender);
}

void parse_ev_fds(IPC_t ipc, char *fds_str)
{
	sscanf(fds_str, "%d-%d", &ipc->evfd_receiver, &ipc->evfd_sender);
	//DBG("[CHILD] %d %d\n", ipc->evfd_receiver, ipc->evfd_sender);
}
