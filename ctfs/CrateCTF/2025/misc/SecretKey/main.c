#include <asm/unistd.h>
#include <errno.h>
#include <inttypes.h>
#include <linux/perf_event.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/random.h>
#include <sys/types.h>
#include <unistd.h>

static long perf_event_open(struct perf_event_attr *hw_event, pid_t pid,
                            int cpu, int group_fd, unsigned long flags) {
  int ret;

  ret = syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
  return ret;
}

bool key_cmp(const char *a, const char *b, int length) {
  for (int i = 0; i < length; i++) {
    if (a[i] != b[i])
      return false;
  }
  return true;
}

int main() {
  struct perf_event_attr pe;
  long long count;
  int fd;
  const char *key = getenv("KEY");
  const char *flag = getenv("FLAG");
  if (key == NULL) {
    printf("Key is null\n");
    exit(-1);
  }

  char buf[256];
  setvbuf(stdout, NULL, _IONBF, 0);
  while (true) {
    printf("Lösenord: ");
    fgets(buf, sizeof(buf), stdin);
    buf[strcspn(buf, "\n")] = 0;

    memset(&pe, 0, sizeof(struct perf_event_attr));
    pe.type = PERF_TYPE_HARDWARE;
    pe.size = sizeof(struct perf_event_attr);
    pe.config = PERF_COUNT_HW_INSTRUCTIONS;
    pe.disabled = 1;
    pe.exclude_kernel = 1;
    // Don't count hypervisor events.
    pe.exclude_hv = 1;

    fd = perf_event_open(&pe, 0, -1, -1, 0);
    if (fd == -1) {
      fprintf(stderr, "Error opening leader %s\n", strerror(errno));
      exit(EXIT_FAILURE);
    }
    if (ioctl(fd, PERF_EVENT_IOC_RESET, 0) == -1)
      fprintf(stderr, "PERF_EVENT_IOC_RESET");
    if (ioctl(fd, PERF_EVENT_IOC_ENABLE, 0) == -1)
      fprintf(stderr, "PERF_EVENT_IOC_ENABLE");

    if (key_cmp(buf, key, strlen(key))) {
      printf("Resurs: %s\n", flag);
      break;
    }
    // inget konstigt här
    uint8_t r;
    getrandom(&r, 1, 0);
    if (r & 1) {
      for (volatile int i = 0; i < 256; i++) {
      }
    }

    if (ioctl(fd, PERF_EVENT_IOC_DISABLE, 0) == -1)
      fprintf(stderr, "PERF_EVENT_IOC_DISABLE");
    if (read(fd, &count, sizeof(count)) != sizeof(count))
      fprintf(stderr, "read");

    close(fd);
    printf("Fel lösenord!\nUtförde en check som tog %llu CPU-instruktioner\n",
           count);
  }
}
