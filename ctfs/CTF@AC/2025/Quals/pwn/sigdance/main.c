#include <dlfcn.h>
#include <pthread.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>

static volatile sig_atomic_t ac = 0, uc = 0;
static void h_alrm(int s) {
  (void)s;
  ac++;
}
static void h_usr1(int s) {
  (void)s;
  uc++;
}

static void *th(void *arg) {
  pid_t pid = *(pid_t *)arg;
  struct timespec ts = {0, 5000000};
  for (int i = 0; i < 13; i++) {
    nanosleep(&ts, NULL);
    kill(pid, SIGUSR1);
  }
  return NULL;
}

static void compute_counts(unsigned *A, unsigned *U) {
  ac = 0;
  uc = 0;
  sigset_t unb;
  sigemptyset(&unb);
  sigaddset(&unb, SIGALRM);
  sigaddset(&unb, SIGUSR1);
  pthread_sigmask(SIG_UNBLOCK, &unb, NULL);

  struct sigaction sa1;
  memset(&sa1, 0, sizeof(sa1));
  sigemptyset(&sa1.sa_mask);
  sa1.sa_flags = SA_RESTART;
  sa1.sa_handler = h_alrm;
  sigaction(SIGALRM, &sa1, NULL);
  struct sigaction sa2;
  memset(&sa2, 0, sizeof(sa2));
  sigemptyset(&sa2.sa_mask);
  sa2.sa_flags = SA_RESTART;
  sa2.sa_handler = h_usr1;
  sigaction(SIGUSR1, &sa2, NULL);

  struct itimerval it;
  it.it_value.tv_sec = 0;
  it.it_value.tv_usec = 7000;
  it.it_interval.tv_sec = 0;
  it.it_interval.tv_usec = 7000;
  setitimer(ITIMER_REAL, &it, NULL);

  pthread_t t;
  pid_t me = getpid();
  pthread_create(&t, NULL, th, &me);

  struct timespec s = {0, 777000000};
  nanosleep(&s, NULL);

  setitimer(ITIMER_REAL, &(struct itimerval){0}, NULL);
  pthread_join(t, NULL);

  *A = (unsigned)ac;
  *U = (unsigned)uc;
}

int main() {
  unsigned A, U;
  compute_counts(&A, &U);
  uint32_t PID = (uint32_t)getpid();
  srand((unsigned)time(NULL) ^ PID ^ A ^ U);
  printf("Hello from pid8 = %u\n", (unsigned)(PID & 255u));
  fflush(stdout);

  void *h = dlopen("./libcore.so", RTLD_NOW | RTLD_LOCAL);
  if (!h)
    return 2;
  int (*verify)(uint32_t, uint32_t, uint32_t, uint32_t) = dlsym(h, "verify");
  if (!verify)
    return 3;

  char buf[256];
  while (fgets(buf, sizeof(buf), stdin)) {
    char *e = buf;
    uint32_t prov = strtoul(buf, &e, 0);
    int ok = verify(prov, (uint32_t)A, (uint32_t)U, PID);
    if (ok) {
      const char *f = getenv("FLAG");
      if (!f)
        f = "FLAG{missing}";
      puts(f);
      dlclose(h);
      return 0;
    } else {
      puts("nope");
      fflush(stdout);
    }
  }
  dlclose(h);
  return 0;
}
