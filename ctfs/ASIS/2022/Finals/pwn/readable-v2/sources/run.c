#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <sys/socket.h>
#include <linux/seccomp.h>
#include "seccomp-bpf.h"

int sockPair[2];
uint8_t skipped_first_req = 0;

int seccomp(unsigned int operation, unsigned int flags, void *args){
  return syscall(__NR_seccomp, operation, flags, args);
}

int sendfd(int sockfd, int fd){
  struct msghdr msgh;
  struct iovec iov;
  int data;
  struct cmsghdr *cmsgp;
  union {
    char   buf[CMSG_SPACE(sizeof(int))];
    struct cmsghdr align;
  } controlMsg;
  msgh.msg_name = NULL;
  msgh.msg_namelen = 0;
  msgh.msg_iov = &iov;
  msgh.msg_iovlen = 1;
  iov.iov_base = &data;
  iov.iov_len = sizeof(int);
  data = 12345;
  msgh.msg_control = controlMsg.buf;
  msgh.msg_controllen = sizeof(controlMsg.buf);
  cmsgp = CMSG_FIRSTHDR(&msgh);
  cmsgp->cmsg_level = SOL_SOCKET;
  cmsgp->cmsg_type = SCM_RIGHTS;
  cmsgp->cmsg_len = CMSG_LEN(sizeof(int));
  memcpy(CMSG_DATA(cmsgp), &fd, sizeof(int));
  if (sendmsg(sockfd, &msgh, 0) == -1){ return -1; }
  return 0;
}

int recvfd(int sockfd)
{
  struct msghdr msgh;
  struct iovec iov;
  int data, fd;
  ssize_t nr;
  union {
    char   buf[CMSG_SPACE(sizeof(int))];
    struct cmsghdr align;
  } controlMsg;
  struct cmsghdr *cmsgp;
  msgh.msg_name = NULL;
  msgh.msg_namelen = 0;
  msgh.msg_iov = &iov;
  msgh.msg_iovlen = 1;
  iov.iov_base = &data;       
  iov.iov_len = sizeof(int);
  msgh.msg_control = controlMsg.buf;
  msgh.msg_controllen = sizeof(controlMsg.buf);
  nr = recvmsg(sockfd, &msgh, 0);
  if (nr == -1){ return -1; }
  cmsgp = CMSG_FIRSTHDR(&msgh);
  if (cmsgp == NULL || 
    cmsgp->cmsg_len != CMSG_LEN(sizeof(int)) ||
    cmsgp->cmsg_level != SOL_SOCKET ||
    cmsgp->cmsg_type != SCM_RIGHTS) {
    errno = EINVAL;
    return -1;
  }
  memcpy(&fd, CMSG_DATA(cmsgp), sizeof(int));
  return fd;
}

int setup_seccomp(){
  int fd;
  struct sock_filter filter[] = {
    VALIDATE_ARCHITECTURE,
    EXAMINE_SYSCALL,
    DISALLOW_SYSCALL(ptrace),
    DISALLOW_SYSCALL(execveat),
    NOTIF_SYSCALL(execve),
    ALLOW_STMT
  };

  struct sock_fprog prog = {
    .len = (unsigned short)(sizeof(filter)/sizeof(filter[0])),
    .filter = filter,
  };

  if ((fd = seccomp(SECCOMP_SET_MODE_FILTER, SECCOMP_FILTER_FLAG_NEW_LISTENER, &prog)) == -1) {
    perror("seccomp");
    return -1;
  }
  return fd;
}

int init_stuff(){
  setbuf(stdout,NULL);
  setbuf(stdin,NULL);
  setbuf(stderr,NULL);
  srand(time(0));
  if(socketpair(AF_UNIX, SOCK_STREAM, 0, sockPair) == -1){
    perror("socketpair()");
    return 1;
  }
  return 0;
}

void closeFdSocks(){
  close(sockPair[0]);
  close(sockPair[1]);
}

void child_handler(char *file_path){
  int listener_fd;
  char *const *n = 0;

  listener_fd = setup_seccomp();
  if(sendfd(sockPair[0],listener_fd)){ perror("sendfd [child]"); return; }
  closeFdSocks();
  if(setgid(1337) || setuid(1337) || close(2)){ return; }

  execve(file_path,n,n);
  exit(1);
}

void allocSeccompNotifBuffers(struct seccomp_notif **req, 
                struct seccomp_notif_resp **resp, 
                struct seccomp_notif_sizes *sizes){
  if (seccomp(SECCOMP_GET_NOTIF_SIZES, 0, sizes) == -1){
    perror("seccomp(SECCOMP_GET_NOTIF_SIZES)");
    exit(1);
  }

  *req = malloc(sizes->seccomp_notif);
  if (*req == NULL){
     puts("err: malloc-seccomp_notif");
     exit(1);
  }

  size_t resp_size = sizes->seccomp_notif_resp;
  if (sizeof(struct seccomp_notif_resp) > resp_size){
     resp_size = sizeof(struct seccomp_notif_resp);
  }

  *resp = malloc(resp_size);
  if (resp == NULL){
     puts("err: malloc-seccomp_notif_resp");
     exit(1);
  }
}

int open_pid_mem(int pid){
  char path[0x100];
  int fd;

  snprintf(path,0x100,"/proc/%d/mem",pid);
  return open(path,0);
}

char *read_path(int pid, uint64_t pid_file_path){
  int mem_fd;
  int pos;
  char *file_path; 

  mem_fd = open_pid_mem(pid);

  if(mem_fd >= 0){
    if(lseek(mem_fd, pid_file_path, SEEK_SET) == -1){ return 0; }
    file_path = malloc(0x1000);
    if(!file_path){ return 0; }
    pos = 0;
    memset(file_path,'\x00',0x1000);
    while(1){
      if(pos >= 0x1000-1 || read(mem_fd,file_path+pos,1) != 1){
        break;
      }
      if(file_path[pos] == '\x00'){ break; }
      pos += 1;
    }
    close(mem_fd);
    return file_path;
  }
  return 0;
}

int process_execute_request(char *file_path, int listener_fd){
  int child_fd;
  char *const *envp = 0;
  char *argv[3] = {
    "/home/pwn/run",
    file_path,
    0
  };

  if((child_fd = fork()) == -1){
    perror("fork");
    return 1;
  } else if(child_fd > 0){
    return 0;
  } else {
    if(close(listener_fd)){ goto failed; };

    // TODO: Implement argv and envp...
    execve("/home/pwn/run",argv,envp);
    failed:
    perror("error while processing execve request");
    exit(1);
  }
}

void handleNotifications(int listener_fd){
  struct seccomp_notif_sizes sizes;
  struct seccomp_notif *req;
  struct seccomp_notif_resp *resp;
  char *file_path;

  allocSeccompNotifBuffers(&req, &resp, &sizes);

  for (;;) {
    memset(req, 0, sizes.seccomp_notif);
    if (ioctl(listener_fd, SECCOMP_IOCTL_NOTIF_RECV, req) == -1) {
      if (errno == EINTR){ continue; }
      puts("err: ioctl-SECCOMP_IOCTL_NOTIF_RECV");
      exit(1);
    }

    resp->id = req->id;
    resp->flags = 0;
    resp->val = 0;
    resp->error = 0;

    if(!skipped_first_req){
      skipped_first_req = 1;
      resp->flags = SECCOMP_USER_NOTIF_FLAG_CONTINUE;
      goto send_response;
    }

    file_path = read_path(req->pid,req->data.args[0]);
    if(file_path){
      resp->error = 0;
      process_execute_request(file_path, listener_fd);
      free(file_path);
      kill(req->pid, 9);
    } 

    send_response:
    if (ioctl(listener_fd, SECCOMP_IOCTL_NOTIF_SEND, resp) == -1) {
      perror("ioctl-notifyfd failed for some reason");
    }
  }

  exit(1);
}

void parent_handler(){
  int listener_fd;
  listener_fd = recvfd(sockPair[1]);
  if(listener_fd == -1){ perror("listener_fd"); return;}
  closeFdSocks();
  handleNotifications(listener_fd);
}

int main(int argc,char *argv[]){
  int child_fd;

  if(argc != 2 || init_stuff()){ return 1; }
 
  if((child_fd = fork()) == -1){
    perror("fork");
    return 1;
  } else if(child_fd > 0){
    parent_handler();
  } else {
    child_handler(argv[1]);
  }
  return 0;
}