#include <err.h>
#include <string.h>
#include <unistd.h>

#include <iostream>
#include <iterator>
#include <fstream>

#include "api.h"
#include "reference_drivers/multiprocess_reference_driver.h"

struct IpczAPI ipcz_api = {
    .size = sizeof(ipcz_api),
};

void CheckIPCZ(IpczResult result, const char* fn) {
  if (result != IPCZ_RESULT_OK) {
    errx(1, "%s failed with error %d", fn, result);
  }
}

int check(int res, const char* msg) {
  if (res == -1)
    err(1, "%s", msg);
  return res;
}

IpczHandle node;

void Get(IpczHandle portal, char* buf, uint32_t* buf_len) {
  while (true) {
    IpczResult result = ipcz_api.Get(portal, IPCZ_NO_FLAGS, nullptr, buf,
                                     buf_len, nullptr, nullptr);
    if (result == IPCZ_RESULT_UNAVAILABLE) {
      usleep(1000);
      continue;
    }
    CheckIPCZ(result, "Get");
    return;
  }
}

void Put(IpczHandle portal, const char* buf, uint32_t buf_len) {
  CheckIPCZ(
      ipcz_api.Put(portal, buf, buf_len, nullptr, 0, IPCZ_NO_FLAGS, nullptr),
      "Put");
}

int main(int argc, char* argv[]) {
  std::ifstream ifs("/flag");
  std::string flag(std::istreambuf_iterator<char>{ifs}, {});

  CheckIPCZ(IpczGetAPI(&ipcz_api), "IpczGetAPI");
  CheckIPCZ(ipcz_api.CreateNode(
                &ipcz::reference_drivers::kMultiprocessReferenceDriver,
                IPCZ_INVALID_DRIVER_HANDLE, IPCZ_NO_FLAGS, NULL, &node),
            "CreateNode");
  IpczHandle portal;
  ipcz::reference_drivers::Channel channel(
      ipcz::reference_drivers::OSHandle(137));
  CheckIPCZ(
      ipcz_api.ConnectNode(
          node,
          ipcz::reference_drivers::CreateTransportFromChannel(
              std::move(channel), ipcz::reference_drivers::OSProcess(),
              ipcz::reference_drivers::MultiprocessTransportSource::
                  kFromNonBroker,
              ipcz::reference_drivers::MultiprocessTransportTarget::kToBroker),
          1, IPCZ_CONNECT_NODE_TO_BROKER, nullptr, &portal),
      "ConnectNode");
  while (1) {
    char buf[1024];
    uint32_t buf_len = sizeof(buf);
    Get(portal, buf, &buf_len);

    if (memcmp(buf, "GetFlag", 7)) {
      std::cout << "ERROR: got " << std::string(buf, buf_len) << std::endl;
      continue;
    }

    Put(portal, flag.data(), flag.size());
  }
}
