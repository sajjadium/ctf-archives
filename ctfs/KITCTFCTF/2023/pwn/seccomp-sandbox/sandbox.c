#define _GNU_SOURCE
#include <errno.h>
#include <linux/audit.h>
#include <seccomp.h>
#include <linux/unistd.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <sys/prctl.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <fcntl.h>


int run_sandbox(int sockfd) {
    scmp_filter_ctx *ctx;
    int fd;
    ctx = seccomp_init(SCMP_ACT_ALLOW);
    //if (seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(mount), 0)) {
    //    perror("seccomp_rule_add");
    //    return 1;
    //}

    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(mount), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(unshare), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(openat2), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(open_by_handle_at), 0);
    seccomp_rule_add(ctx, SCMP_ACT_NOTIFY, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_NOTIFY, SCMP_SYS(openat), 0);

    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(link), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(symlink), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(linkat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(symlinkat), 0);

    // prevent notification bypass through registration of higher precedence filters
    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(prctl), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ERRNO(1), SCMP_SYS(seccomp), 0);

    if (seccomp_load(ctx)) {
        perror("seccomp_load");
        return 1;
    }

    fd = seccomp_notify_fd(ctx);
#ifdef DEBUG
    printf("fd: %d\n", fd);
#endif

    // send notification file descriptor
    // (just a bunch of boilerplate code blindly copied from https://stackoverflow.com/a/28005250)
    struct msghdr msg = { 0 };
    char buf[CMSG_SPACE(sizeof(fd))];
    memset(buf, '\0', sizeof(buf));
    struct iovec io = { .iov_base = "ABC", .iov_len = 3 };
    msg.msg_iov = &io;
    msg.msg_iovlen = 1;
    msg.msg_control = buf;
    msg.msg_controllen = sizeof(buf);
    struct cmsghdr * cmsg = CMSG_FIRSTHDR(&msg);
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type = SCM_RIGHTS;
    cmsg->cmsg_len = CMSG_LEN(sizeof(fd));
    *((int *) CMSG_DATA(cmsg)) = fd;
    msg.msg_controllen = CMSG_SPACE(sizeof(fd));
    if (sendmsg(sockfd, &msg, 0) < 0) {
        perror("Failed to send message\n");
        return 1;
    }


    // spawn shell
    if (execl("/bin/bash", "/bin/bash",NULL)) {
        perror("execl");
        return 1;
    }
    return 0;
}

int install_monitor(int sockfd, int pid) {
    // receive notification file descriptor
    // (just a bunch of boilerplate code blindly copied from https://stackoverflow.com/a/28005250)
    struct msghdr msg = {0};
    char m_buffer[256];
    struct iovec io = { .iov_base = m_buffer, .iov_len = sizeof(m_buffer) };
    msg.msg_iov = &io;
    msg.msg_iovlen = 1;
    char c_buffer[256];
    msg.msg_control = c_buffer;
    msg.msg_controllen = sizeof(c_buffer);
    if (recvmsg(sockfd, &msg, 0) < 0) {
        perror("Failed to receive message\n");
        return 1;
    }
    struct cmsghdr * cmsg = CMSG_FIRSTHDR(&msg);
    unsigned char * data = CMSG_DATA(cmsg);
#ifdef DEBUG
    printf("About to extract fd\n");
#endif
    int fd = *((int*) data);
#ifdef DEBUG
    printf("Extracted fd %d\n", fd);
#endif


    // listen for and handle notifications
    while (1) {
        struct seccomp_notif *req;
        struct seccomp_notif_resp *resp;
        seccomp_notify_alloc(&req, &resp);
        seccomp_notify_receive(fd, req);

        //// exit if child has exited
        //int wstatus;
        //waitpid(0, &wstatus, WNOHANG);
        //if (WIFEXITED(wstatus)) {
        //    printf("child exited\n");
        //    break;
        //}

#ifdef DEBUG
        printf("received %d\n", req->data.nr);
#endif
#ifdef DEBUG2
        printf("dirfd: %d\npath: 0x%llx\nflags: %x\nmode: %x\n",
               (int)req->data.args[0],
               req->data.args[1],
               (int)req->data.args[2],
               (int)req->data.args[3]);
#endif

        resp->id = req->id;

        if (req->data.nr == SCMP_SYS(openat) || req->data.nr == SCMP_SYS(open)) {
            uint64_t addr;
            int memfd;
            char *mempath;
            char buf[4096];

            if (req->data.nr == SCMP_SYS(open)) {
                addr = req->data.args[0];
            }
            else { // req->data.nr == SCMP_SYS(openat)
                addr = req->data.args[1];
            }

            asprintf(&mempath, "/proc/%d/mem", req->pid);
            memfd = open(mempath, O_RDONLY);
            free(mempath);
            if (memfd < 0) {
                perror("open");
                continue;
            }
            lseek(memfd, addr, SEEK_SET);
            // missing null byte?
            if (read(memfd, buf, 4096) == -1) {
                perror("read");
                close(memfd);
                continue;
            }
            close(memfd);

#ifdef DEBUG
            printf("read: %s\n", buf);
#endif
            if (strstr(buf, "flag") != NULL) {
                printf("Tried to access forbidden file!\n");
                resp->error = -EPERM;
            }
            else {
                resp->flags = SECCOMP_USER_NOTIF_FLAG_CONTINUE;
            }
        }
        else {
            resp->error = -EPERM;
        }

        seccomp_notify_respond(fd, resp);
        seccomp_notify_free(req, resp);
    }
    return fd;
}

int main(int argc, char *argv[]) {
    int sockPair[2];
    if (socketpair(AF_UNIX, SOCK_STREAM, 0, sockPair) == -1) {
        perror("socketpair");
        return 1;
    }

    int pid = fork();
    if (pid > 0) { // in parent
        install_monitor(sockPair[0], pid);
    }
    else { // in child
        if (run_sandbox(sockPair[1])) {
            return 1;
        }
    }
    //return EXIT_SUCCESS;
    return 0;
}
