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

void initDevice() {
  uint64_t readSize;
  uint8_t tmp;
  while (true) {
    pollFd(DV_READ_FD, true);
    if ((readSize = read(DV_READ_FD, &tmp, 1)) != 1) {
      if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) printError("initDevice::read failed");
    } else {
      break;
    }
  }
  if (tmp != 0xff) printError("initDevice::sync code incorrect");
  if (write(DV_WRITE_FD, &tmp, 1) != 1) printError("initDevice::write failed");
  if (write(DV_INTERRUPT_FD, &tmp, 1) != 1) printError("initDevice::write failed");
  return;
}

void dv_sendMsg(uint8_t type, uint8_t *msg, uint64_t size) {
  if (write(DV_WRITE_FD, &type, 1) != 1) printError("dv_sendMsg::write failed");
  if (write(DV_WRITE_FD, msg, size) != size) printError("dv_sendMsg::write failed");
  return;
}

uint8_t dv_recvMsg(uint8_t *res, bool block) {
  uint64_t totalSize;
  int readSize;
  uint8_t type;
  if (pollFd(DV_READ_FD, block) == 0) return DV_NO_MSG;
  if ((readSize = read(DV_READ_FD, &type, 1)) != 1) {
    if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) printError("dv_recvMsg::read failed");
    return DV_NO_MSG;
  }
  switch (type) {
    case DV_APPLET_REGISTER_MSG:
      totalSize = sizeof(DEVICE_APPLET);
      break;
    case DV_APPLET_INVOKE_MSG:
      totalSize = sizeof(DEVICE_APPLET_INVOKE);
      break;
    case DV_APPLET_RESUME_MSG:
      totalSize = sizeof(DEVICE_APPLET_RESUME);
      break;
    default:
      printError("dv_recvMsg::unknown msg");
  }
  for (uint64_t cursor = 0; cursor < totalSize; cursor += readSize) {
    pollFd(DV_READ_FD, true);
    if ((readSize = read(DV_READ_FD, &res[cursor], totalSize - cursor)) <= 0) {
      if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) printError("dv_recvMsg::read failed");
      readSize = 0;
    }
  }
  return type;
}

void dv_sendInterrupt(uint8_t type, uint8_t *msg, uint64_t size) {
  if (write(DV_INTERRUPT_FD, &type, 1) != 1) printError("dv_sendInterrupt::write failed");
  if (write(DV_INTERRUPT_FD, msg, size) != size) printError("dv_sendInterrupt::write failed");
  return;
}
