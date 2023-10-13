#include <unistd.h>
int main() {
  setuid(0);
  char *newargv[] = { "/bin/cat", "/flag", NULL };
  char *newenviron[] = { NULL };
  execve("/bin/cat", newargv, newenviron);
}