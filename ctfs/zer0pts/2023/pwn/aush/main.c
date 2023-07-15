#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#define LEN_USER 0x10
#define LEN_PASS 0x20

int setup(char *passbuf, size_t passlen, char *userbuf, size_t userlen) {
  int ret, fd;

  // TODO: change it to password/username file
  if ((fd = open("/dev/urandom", O_RDONLY)) == -1)
    return 1;
  ret  = read(fd, passbuf, passlen) != passlen;
  ret |= read(fd, userbuf, userlen) != userlen;
  close(fd);
  return ret;
}

int main(int argc, char **argv, char **envp) {
  char *args[3];
  char inpuser[LEN_USER+1] = { 0 };
  char inppass[LEN_PASS+1] = { 0 };
  char username[LEN_USER] = { 0 };
  char password[LEN_PASS] = { 0 };

  if (system("/usr/games/cowsay Welcome to AUSH: AUthenticated SHell!") != 0) {
    write(STDOUT_FILENO, "cowsay not found\n", 17);
    return 1;
  }

  /* Load password and username file */
  if (setup(password, LEN_PASS, username, LEN_USER))
    return 1;

  /* Check username */
  write(STDOUT_FILENO, "Username: ", 10);
  if (read(STDIN_FILENO, inpuser, 0x200) <= 0)
    return 1;

  if (memcmp(username, inpuser, LEN_USER) != 0) {
    args[0] = "/usr/games/cowsay";
    args[1] = "Invalid username";
    args[2] = NULL;
    execve(args[0], args, envp);
  }

  /* Check password */
  write(STDOUT_FILENO, "Password: ", 10);
  if (read(STDIN_FILENO, inppass, 0x200) <= 0)
    return 1;

  if (memcmp(password, inppass, LEN_PASS) != 0) {
    args[0] = "/usr/games/cowsay";
    args[1] = "Invalid password";
    args[2] = NULL;
    execve(args[0], args, envp);
  }

  /* Grant access */
  args[0] = "/bin/sh";
  args[1] = NULL;
  execve(args[0], args, envp);
  return 0;
}
