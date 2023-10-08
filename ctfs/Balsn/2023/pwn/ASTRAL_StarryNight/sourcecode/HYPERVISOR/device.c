#include "device.h"

uint64_t pollFd(int fd, bool block) {
  struct pollfd pfd;
  uint64_t res;
  pfd.fd = fd;
  pfd.events = POLLIN;
  pfd.revents = 0;
  if ((res = poll(&pfd, 1, block ? -1 : 0)) == -1) printError("pollFd::poll failed");
  return res;
}

void launchDevice(char *device, char *timeout) {
  int deviceFd[3][2];
  if (pipe2(deviceFd[0], O_NONBLOCK) == -1) printError("launchDevice::pipe2 failed");
  if (pipe2(deviceFd[1], O_NONBLOCK) == -1) printError("launchDevice::pipe2 failed");
  if (pipe2(deviceFd[2], O_NONBLOCK) == -1) printError("launchDevice::pipe2 failed");
  pid_t pid = fork();
  if (pid < 0) printError("launchDevice::fork failed");
  else if (pid == 0) {
    //child
    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);
    close(deviceFd[0][0]);
    close(deviceFd[1][1]);
    close(deviceFd[2][0]);
    if (dup2(deviceFd[0][1], DV_WRITE_FD) == -1) printError("launchDevice::dup failed");
    if (dup2(deviceFd[1][0], DV_READ_FD) == -1) printError("launchDevice::dup failed");
    if (dup2(deviceFd[2][1], DV_INTERRUPT_FD) == -1) printError("launchDevice::dup failed");
    close(deviceFd[0][1]);
    close(deviceFd[1][0]);
    close(deviceFd[2][1]);
    char *argv[] = {"/usr/bin/timeout", timeout, device, NULL};
    if (execve(argv[0], argv, NULL) == -1) printError("launchDevice::execve failed");
    _exit(0);
  } else {
    //parent
    close(deviceFd[0][1]);
    close(deviceFd[1][0]);
    close(deviceFd[2][1]);
    if (dup2(deviceFd[0][0], DV_READ_FD) == -1) printError("launchDevice::dup failed");
    if (dup2(deviceFd[1][1], DV_WRITE_FD) == -1) printError("launchDevice::dup failed");
    if (dup2(deviceFd[2][0], DV_INTERRUPT_FD) == -1) printError("launchDevice::dup failed");
    close(deviceFd[0][0]);
    close(deviceFd[1][1]);
    close(deviceFd[2][0]);
    uint64_t readSize;
    uint8_t tmp = DV_SYNC_CODE;
    if (write(DV_WRITE_FD, &tmp, 1) != 1) printError("launchDevice::write failed");
    while (true) {
      pollFd(DV_READ_FD, true);
      if ((readSize = read(DV_READ_FD, &tmp, 1)) != 1) {
        if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) printError("launchDevice::read failed");
      } else {
        break;
      }
    }
    if (tmp != DV_SYNC_CODE) printError("launchDevice::sync code incorrect");
    while (true) {
      pollFd(DV_INTERRUPT_FD, true);
      if ((readSize = read(DV_INTERRUPT_FD, &tmp, 1)) != 1) {
        if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) printError("launchDevice::read failed");
      } else {
        break;
      }
    }
    if (tmp != DV_SYNC_CODE) printError("launchDevice::sync code incorrect");
  }
  return;
}

void dv_sendMsg(uint8_t type, uint8_t *msg, uint64_t size) {
  if (write(DV_WRITE_FD, &type, 1) != 1) printError("dv_sendMsg::write failed");
  if (write(DV_WRITE_FD, msg, size) != size) printError("dv_sendMsg::write failed");
  return;
}

void dv_recvMsg(uint8_t type, uint8_t *msg, uint64_t size) {
  //recvMsg is synchronous, thus type can be fully anticipated 
  int readSize;
  uint8_t rType;
  while (true) {
    pollFd(DV_READ_FD, true);
    if ((readSize = read(DV_READ_FD, &rType, 1)) != 1) {
      if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) printError("dv_recvMsg::read failed");
    } else {
      break;
    }
  }
  if (rType != type) printError("dv_recvMsg::incorrect type");
  for (uint64_t cursor = 0; cursor < size; cursor += readSize) {
    pollFd(DV_READ_FD, true);
    if ((readSize = read(DV_READ_FD, &msg[cursor], size - cursor)) <= 0) {
      if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) printError("dv_recvMsg::read failed");
      readSize = 0;
    }
  }
  return;
}

uint8_t dv_recvInterrupt(uint8_t *res) {
  uint64_t totalSize;
  int readSize;
  uint8_t type;
  if (pollFd(DV_INTERRUPT_FD, false) == 0) return DV_NO_INTERRUPT;
  if ((readSize = read(DV_INTERRUPT_FD, &type, 1)) != 1) {
    if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) printError("dv_recvInterrupt::read failed");
    //There are no msg queued, we can just return
    return DV_NO_INTERRUPT;
  }
  //size does not include type,
  switch (type) {
    case DV_APPLET_RES_INTERRUPT:
      totalSize = sizeof(HYPER_APPLET_RES);
      break;
    case DV_APPLET_INVOKE_INTERRUPT:
      totalSize = sizeof(HYPER_APPLET_CONTEXT);
      break;
    case DV_APPLET_PROCESSOR_FLAG_INTERRUPT:
      totalSize = 0;
      break;
    default:
      printError("dv_recvInterrupt::unknown interrupt");
  }
  for (uint64_t cursor = 0; cursor < totalSize; cursor += readSize) {
    pollFd(DV_INTERRUPT_FD, true);
    if ((readSize = read(DV_INTERRUPT_FD, &res[cursor], totalSize - cursor)) <= 0) {
      if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) printError("dv_recvInterrupt::read failed");
      readSize = 0;
    }
  }
  return type;
}
