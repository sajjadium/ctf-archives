#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/types.h>
#include <errno.h>
#include <sys/wait.h>

/*
 * A workaround to communicate with our program via socket.
 */
int main(int argc, char **argv, char **envp){
    int pipefd[2];
    int pid;
    char *args[] = {"/bin/sh", "-c", "node chall.js", NULL};
    char buf[256];
    ssize_t len;

    if(pipe(pipefd) < 0){
        perror("pipe");
        exit(1);
    }

    pid = fork();
    if(pid < 0){
        perror("fork");
        exit(1);
    }

    if(pid == 0){
        // child
        close(pipefd[1]);
        dup2(pipefd[0], 0);
        dup2(1, 2);
        execve(args[0], args, envp);

        perror("execve");
        exit(1);
    }

    // parent
    close(pipefd[0]);
    dup2(pipefd[1], 1);

    while(1){
        len = read(0, buf, sizeof(buf));
        if(len <= 0){
            if(errno == EAGAIN || errno == EINTR){
                usleep(100);
                continue;
            }
            break;
        }
        if(write(1, buf, len) <= 0){
            break;
        }
    }

    kill(pid, SIGTERM);
    waitpid(pid, NULL, 0);

    return 0;
}
