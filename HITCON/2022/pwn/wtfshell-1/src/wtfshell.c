#define _GNU_SOURCE
#include <fcntl.h>
#include <limits.h>
#include <linux/filter.h>
#include <linux/seccomp.h>
#include <linux/unistd.h>
#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/prctl.h>
#include <sys/uio.h>
#include <unistd.h>

#define GBSIZE 0x400
#define SBSIZE 0x100
#define FILEMAX 0x80
#define USERMAX 0x10
#define PWMAX 0x40
#define DIGITMAX 0x80

#define RDPERM 0x2
#define WRPERM 0x1

struct file {
    char *fname;
    char *fdata;
    int fuid;
    int fflag;
};

struct user {
    char ushadow[PWMAX];
    char *uname;
    int uid;
};

const char ps_user[] = "e ";
const char ps_root[] = "√ ";
const char delim[] = ".,?!";
char *gbuff;
int curr_uid;
struct file *gfiles[FILEMAX];
struct user *gusers[USERMAX];

int comm_fd;
int cmdline_fd;

void terminate() {
    _exit(EXIT_FAILURE);
}

/* dynamic memory allocation wrappers */

void *xmalloc(int size) {
    if (size == 0) {
        size = 1;
    }
    void *ptr = malloc(size);
    bzero(ptr, size);
    return ptr;
}

void *xrealloc(void *ptr, int size) {
    if (size == 0) {
        size = 1;
    }
    return realloc(ptr, size);
}

void xfree(void *ptr) {
    if (!ptr) {
        return;
    }
    size_t size = malloc_usable_size(ptr);
    bzero(ptr, size);
    free(ptr);
}

/* IO wrappers */

int read_max(char *dest, const size_t max_len) {
    int read_num = 0;
    while (read_num < max_len) {
        int res = read(STDIN_FILENO, &dest[read_num], 1);
        if (res < 0) {
            terminate();
        }
        if (dest[read_num] == '\n') {
            dest[read_num] = '\0';
            return read_num;
        }
        read_num++;
    }
    return read_num;
}

int write_max(const char *dest, const size_t max_len) {
    int write_num = 0;
    struct iovec iov;
    while (write_num < max_len) {
        iov.iov_base = (char *)&dest[write_num];
        iov.iov_len = 1;
        int res = writev(STDOUT_FILENO, &iov, 1);
        if (res < 0) {
            terminate();
        }
        write_num++;
    }
    return write_num;
}

int write_str(const char *dest) {
    return write_max(dest, strlen(dest));
}

void itoa(int num, char *s) {
    int i, sign;
    if ((sign = num) < 0) {
        num = -num;
    }
    i = 0;
    do {
        s[i++] = num % 10 + '0';
    } while ((num /= 10) > 0);
    if (sign < 0) {
        s[i++] = '-';
    }
    s[i] = '\0';
    for (int j = 0, k = i - 1; j < k; j++, k--) {
        char c = s[j];
        s[j] = s[k];
        s[k] = c;
    }
}

void write_int(const int num) {
    char *tmp = xmalloc(SBSIZE);
    itoa(num, tmp);
    write_str(tmp);
    xfree(tmp);
}

int chk_digit(const char *str) {
    int len = strlen(str);
    for (int i = 0; i < len; i++) {
        if (str[i] < '0' || str[i] > '9') {
            return 0;
        }
    }
    return 1;
}

void remove_slash(char *fname) {
    int fname_len = strlen(fname);
    for (int i = 0; i < fname_len; i++) {
        if (fname[i] == '/') {
            fname[i] = '\0';
        }
    }
}

/* command wrappers */

const char *getnamebyuid(int uid) {
    for (int i = 0; i < USERMAX; i++) {
        if (gusers[i] && gusers[i]->uid == uid) {
            return gusers[i]->uname;
        }
    }
    return NULL;
}

int getuidbyname(const char *uname) {
    for (int i = 0; i < USERMAX; i++) {
        if (gusers[i] && gusers[i]->uname && !strcmp(gusers[i]->uname, uname)) {
            return gusers[i]->uid;
        }
    }
    return -1;
}

int read_pw(char *dest) {
    int read_num = 0;
    while (read_num < PWMAX) {
        int res = read(STDIN_FILENO, &dest[read_num], 1);
        if (res < 0) {
            terminate();
        }
        if (dest[read_num] == '\n') {
            dest[read_num] = '\0';
            return read_num;
        }
        read_num++;
    }
    return read_num;
}

int chk_pw(const char *pw) {
    char input;
    int pw_len = strlen(pw);
    for (int i = 0; i < pw_len + 1; i++) {
        int res = read(STDIN_FILENO, &input, 1); 
        if (res < 0) {
            terminate();
        }
        if (i == pw_len) { // The last character must be a line break
            return input == '\n';
        }
        if (input == '\n') { // Ignore accidental line breaks
            i--;
            continue;
        }
        /* If password mismatch, quit immediately */
        if (input != pw[i]) {
            /* Read characters until '\n' */
            while (1) {
                int res = read(STDIN_FILENO, &input, 1); 
                if (res < 0) {
                    terminate();
                }
                if (input == '\n') {
                    return 0;
                }
            }
        }
    }
}

/* command handlers */

void cmd_rtfm() {
    write_str("πππππππππππππππππππππππππππππππππππππππππππππππππππππππππππππππππ\n");
    write_str("π\trtfm.\t\t\tRead This Friendly Manual\tπ\n");
    write_str("π\tqq.\t\t\tQuit Quietly\t\t\tπ\n");
    write_str("π\tlol,[-l].\t\tList Of fiLes\t\t\tπ\n");
    write_str("π\trip.[FILE]\t\tRedirect InPut\t\t\tπ\n");
    write_str("π\tnsfw,FILE,PERM.\t\tNew Single File for Writing\tπ\n");
    write_str("π\twtf,DATA,FILE.\t\tWrite data To File\t\tπ\n");
    write_str("π\tomfg,FILE.\t\tOutput My File Gracefully\tπ\n");
    write_str("π\tgtfo,FILE.\t\tGeT the File Out\t\tπ\n");
    write_str("π\touo.\t\t\tOutput current User Out\t\tπ\n");
    write_str("π\tstfu,USER.\t\tSeT new Friendly User\t\tπ\n");
    write_str("π\tasap,[USER].\t\tASsign A new Password\t\tπ\n");
    write_str("π\tsus,USER.\t\tSwitch USer\t\t\tπ\n");
    write_str("π\tshit.\t\t\tSHell InformaTion\t\tπ\n");
    write_str("π\tirl.\t\t\tInstantly Reset shelL\t\tπ\n");
    write_str("πππππππππππππππππππππππππππππππππππππππππππππππππππππππππππππππππ\n");
}

void cmd_qq() {
    xfree(gbuff);
    close(comm_fd);
    close(cmdline_fd);
    close(STDERR_FILENO);
    close(STDOUT_FILENO);
    close(STDIN_FILENO);
    _exit(EXIT_SUCCESS);
}

void cmd_lol() {
    char *flag = strtok(NULL, delim);
    int total = 0;
    if (!flag) {
        int first = 1;
        for (int i = 0; i < FILEMAX; i++) {
            if (gfiles[i] && gfiles[i]->fname) {
                if (!first) {
                    write_str("\t");
                }
                write_str(gfiles[i]->fname);
                first = 0;
                total++;
            }
        }
        if (total > 0) {
            write_str("\n");
        }
    } else if (!strcmp(flag, "-l")) {
        int fsize = 0;
        const char *uname;
        for (int i = 0; i < FILEMAX; i++) {
            if (gfiles[i] && gfiles[i]->fname) {
                
                /* Print file permission */
                if (gfiles[i]->fflag & RDPERM) {
                    write_str("r");
                } else {
                    write_str("-");
                }
                if (gfiles[i]->fflag & WRPERM) {
                    write_str("w");
                } else {
                    write_str("-");
                }
                write_str("\t");

                /* Print file ownership */
                uname = getnamebyuid(gfiles[i]->fuid);
                if (uname) {
                    write_str(uname);
                } else {
                    write_str("∅");
                }
                write_str("\t");
                
                /* Print file size */
                if (gfiles[i]->fdata) {
                    fsize = strlen(gfiles[i]->fdata);
                } else {
                    fsize = 0;
                }
                write_int(fsize);
                write_str("\t");

                /* Print file name */
                write_str(gfiles[i]->fname);
                write_str("\n");
                total++;
            }
        }

        /* Print the total number of files */
        write_str("∑ file = ");
        write_int(total);
        write_str("\n");
    } else {
        /* Unrecognized flag */
        write_str("lol: \"");
        write_str(flag);
        write_str("\" ∉ { \"-l\" }");
        write_str("\n");
        return;
    }
}

void cmd_rip() {
    char *fname = strtok(NULL, delim);
    char *rbuff = xmalloc(SBSIZE);

    /* Redirect input to stdout */
    if (!fname) {
        read_max(rbuff, SBSIZE);
        write_str(rbuff);
        write_str("\n");
        xfree(rbuff);
        return;
    }
    
    /* Redirect input to a file */

    remove_slash(fname);
    if (strlen(fname) == 0) {
        write_str("rip: flag = ∅\n");
        xfree(rbuff);
        return;
    }
    /* Special case: flag1 cannot be altered */
    if (!strcmp(fname, "flag1")) {
        write_str("rip: ¬ perm\n");
        xfree(rbuff);
        return;
    }
    for (int i = 1 /* ignore flag1 */; i < FILEMAX; i++) {
        if (gfiles[i] && gfiles[i]->fname && !strcmp(gfiles[i]->fname, fname)) {
            /* The file's owner must be root or the current user, and the file must be writable */
            if ((curr_uid != 0 && gfiles[i]->fuid != curr_uid) || !(gfiles[i]->fflag & WRPERM)) {
                write_str("rip: ¬ perm\n");
                xfree(rbuff);
                return;
            }

            read_max(rbuff, SBSIZE);
            if (gfiles[i]->fdata) {
                /* File is not empty -> rewrite the file content */
                if (strlen(rbuff) > 0) {
                    gfiles[i]->fdata = xrealloc(gfiles[i]->fdata, strlen(gfiles[i]->fdata) + strlen(rbuff) + 1); // Remember the extra null byte
                }
                strcat(gfiles[i]->fdata, rbuff);
            } else {
                /* File is empty -> write the content directly */
                gfiles[i]->fdata = strdup(rbuff);
            }
            xfree(rbuff);
            return;
        }
    }
    write_str("rip: \"");
    write_str(fname);
    write_str("\" ∉ ℱ\n");
    xfree(rbuff);
}

void cmd_nsfw() {
    char *fname = strtok(NULL, delim);
    if (!fname) {
        write_str("nsfw: file = ∅\n");
        return;
    }
    remove_slash(fname);
    if (strlen(fname) == 0) {
        write_str("nsfw: file = ∅\n");
        return;
    }

    char *fflag_s = strtok(NULL, delim);
    if (!fflag_s) {
        write_str("nsfw: flag = ∅\n");
        return;
    }

    /*
     * --: 0 (non-readable & non-writable)
     * -w: 1 (write only)
     * r-: 2 (read only)
     * rw: 3 (readable & writable)
     */
    if (!chk_digit(fflag_s)) {
        write_str("nsfw: \"");
        write_str(fflag_s);
        write_str("\" ∉ ℕ\n");
        return;
    }
    int fflag = atoi(fflag_s);
    if (fflag < 0 || fflag >= 4) {
        write_str("nsfw: flag < 0 ⋁ flag ≥ 4\n");
        return;
    }
    /* Check for existing files */
    for (int i = 0; i < FILEMAX; i++) {
        if (gfiles[i] && gfiles[i]->fname && !strcmp(gfiles[i]->fname, fname)) {
            write_str("nsfw: ∃ file ∈ ℱ s.t. file = \"");
            write_str(fname);
            write_str("\"\n");
            return;
        }
    }
    /* Create a new file */
    for (int i = 0; i < FILEMAX; i++) {
        if (!gfiles[i]) {
            gfiles[i] = xmalloc(sizeof(struct file));
            gfiles[i]->fuid = curr_uid;
            gfiles[i]->fflag = fflag;
            gfiles[i]->fname = strdup(fname);
            gfiles[i]->fdata = NULL;
            return;
        }
    }
    write_str("nsfw: |ℱ| > ");
    write_int(FILEMAX);
    write_str("\n");
}

void cmd_wtf() {
    char *fdata = strtok(NULL, delim);
    if (!fdata) {
        write_str("wtf: data ∈ ∅\n");
        return;
    }
    char *fname = strtok(NULL, delim);
    if (!fname) {
        write_str("wtf: file ∈ ∅\n");
        return;
    }

    remove_slash(fname);
    if (strlen(fname) == 0) {
        write_str("wtf: file = ∅\n");
        return;
    }
    /* Special case: flag1 cannot be altered */
    if (!strcmp(fname, "flag1")) {
        write_str("wtf: ¬ perm\n");
        return;
    }
    for (int i = 1 /* ignore flag1 */; i < FILEMAX; i++) {
        if (gfiles[i] && gfiles[i]->fname && !strcmp(gfiles[i]->fname, fname)) {
            /* The file's owner must be root or the current user, and the file must be writable */
            if ((curr_uid != 0 && gfiles[i]->fuid != curr_uid) || !(gfiles[i]->fflag & WRPERM)) {
                write_str("wtf: ¬ perm\n");
                return;
            }
            if (gfiles[i]->fdata) {
                /* File is not empty -> rewrite the file content */
                if (strlen(fdata) > strlen(gfiles[i]->fdata)) {
                    gfiles[i]->fdata = xrealloc(gfiles[i]->fdata, strlen(fdata) + 1); // Remember the extra null byte
                }
                strcpy(gfiles[i]->fdata, fdata);
            } else {
                /* File is empty -> write the content directly */
                gfiles[i]->fdata = strdup(fdata);
            }
            return;
        }
    }
    write_str("wtf: \"");
    write_str(fname);
    write_str("\" ∉ ℱ\n");
}

void cmd_omfg() {
    char *fname = strtok(NULL, delim);
    if (!fname) {
        write_str("omfg: file ∈ ∅\n");
        return;
    }
    remove_slash(fname);
    if (strlen(fname) == 0) {
        write_str("omfg: file = ∅\n");
        return;
    }
    for (int i = 0; i < FILEMAX; i++) {
        if (gfiles[i] && gfiles[i]->fname && !strcmp(gfiles[i]->fname, fname)) {
            /* The file's owner must be root or the current user, and the file must be readable */
            if ((curr_uid != 0 && gfiles[i]->fuid != curr_uid) || !(gfiles[i]->fflag & RDPERM)) {
                write_str("omfg: ¬ perm\n");
                return;
            }
            if (!gfiles[i]->fdata) { // empty file
                return;
            }
            write_str(gfiles[i]->fdata);
            write_str("\n");
            return;
        }
    }
    write_str("omfg: \"");
    write_str(fname);
    write_str("\" ∉ ℱ \n");
}

void cmd_gtfo() {
    char *fname = strtok(NULL, delim);
    if (!fname) {
        write_str("gtfo: file ∈ ∅\n");
        return;
    }
    remove_slash(fname);
    if (strlen(fname) == 0) {
        write_str("gtfo: file = ∅\n");
        return;
    }
    /* Special case: flag1 cannot be deleted */
    if (!strcmp(fname, "flag1")) {
        write_str("wtf: ¬ perm\n");
        return;
    }
    for (int i = 1 /* ignore flag1 */; i < FILEMAX; i++) {
        if (gfiles[i] && gfiles[i]->fname && !strcmp(gfiles[i]->fname, fname)) {
            /* The file's owner must be root or the current user, and the file must be writable */
            if ((curr_uid != 0 && gfiles[i]->fuid != curr_uid) || !(gfiles[i]->fflag & WRPERM)) {
                write_str("gtfo: ¬ perm\n");
                return;
            }
            /* Free the file name & the file data */
            xfree(gfiles[i]->fname);
            if (gfiles[i]->fdata) {
                xfree(gfiles[i]->fdata);
            }
            xfree(gfiles[i]);
            /* Prevent use-after-free */
            gfiles[i] = NULL;
            return;
        }
    }
    write_str("gtfo: \"");
    write_str(fname);
    write_str("\" ∉ ℱ \n");
}

void cmd_ouo() {
    const char *uname = getnamebyuid(curr_uid);
    if (uname) {
        write_str(uname);
    } else {
        write_str("ouo: user ∈ ∅\n");
        return;
    }
    write_str("\n");
}

void cmd_stfu() {
    if (curr_uid != 0) {
        write_str("stfu: ¬ perm\n");
        return;
    }
    char *uname = strtok(NULL, delim);
    if (!uname) {
        write_str("stfu: user ∈ ∅\n");
        return;
    }
    /* Check for existing users */
    for (int i = 0; i < USERMAX; i++) {
        if (gusers[i] && gusers[i]->uname && !strcmp(gusers[i]->uname, uname)) {
            write_str("stfu: ∃ user ∈ 𝒰 s.t. user = \"");
            write_str(uname);
            write_str("\"\n");
            return;
        }
    }
    /* Create a new user */
    for (int i = 0; i < USERMAX; i++) {
        if (!gusers[i]) {
            gusers[i] = xmalloc(sizeof(struct user));
            gusers[i]->uname = strdup(uname);
            gusers[i]->uid = i;
            return;
        }
    }
    /* Too many users */
    write_str("stfu: |𝒰| > ");
    write_int(USERMAX);
    write_str("\n");
}

void cmd_asap() {
    char *uname = strtok(NULL, delim);
    int uid;
    if (!uname) {
        uid = curr_uid; // the default user is the current user
    } else {
        uid = getuidbyname(uname);
        if (uid == -1) {
            write_str("asap: \"");
            write_str(uname);
            write_str("\" ∉ 𝒰\n");
            return;
        }
    }
    /* Only root or the current user can set password */
    if (curr_uid != 0 && curr_uid != uid) {
        write_str("asap: ¬ perm\n");
        return;
    }
    for (int i = 0; i < USERMAX; i++) {
        if (gusers[i] && gusers[i]->uname && gusers[i]->uid == uid) {
            /* Enter the password */
            write_str("password:");
            /* Enter the password again in case of typo */
            read_pw(gusers[i]->ushadow);
            write_str("retype password:");
            if (!chk_pw(gusers[i]->ushadow)) {
                /* Clear data when error occurs */
                bzero(gusers[i]->ushadow, PWMAX);
                write_str("asap: pw1 ≠ pw2\n");
                return;
            }

            write_str("Q.E.D.\n");
            return;
        }
    }
}

void cmd_sus() {
    char *uname = strtok(NULL, delim);
    int uid;
    if (!uname) {
        uid = 0; // the default user is root
    } else {
        uid = getuidbyname(uname);
        if (uid == -1) {
            write_str("sus: \"");
            write_str(uname);
            write_str("\" ∉ 𝒰\n");
            return;
        }
    }

    /* Special case: password length is zero */
    if (strlen(gusers[uid]->ushadow) == 0) {
        curr_uid = uid;
        return;
    }

    char *enter_pw = xmalloc(SBSIZE);
    write_str("password: ");
    read_pw(enter_pw);

    if (!strcmp(gusers[uid]->ushadow, enter_pw)) {
        write_str("sus: ¬ perm\n");
        xfree(enter_pw);
        return;
    }

    /* set current uid */
    curr_uid = uid;
    xfree(enter_pw);
}

void cmd_shit() {
    int pid = getpid();
    char binary[PATH_MAX] = {};
    char cmdline[PATH_MAX] = {};
    int uid = getuid();
    int gid = getgid();

    struct iovec iov[2];
    iov[0].iov_base = binary;
    iov[0].iov_len = PATH_MAX;
    iov[1].iov_base = cmdline;
    iov[1].iov_len = PATH_MAX;

    if (preadv(comm_fd, &iov[0], 1, 0) < 0) {
        terminate();
    }
    if (preadv(cmdline_fd, &iov[1], 1, 0) < 0) {
        terminate();
    }

    write_str("pid:\t\t");
    write_int(pid);
    write_str("\n");

    write_str("binary:\t\t");
    write_str(binary);

    write_str("cmdline:\t");
    write_str(cmdline);
    write_str("\n");

    write_str("uid:\t\t");
    write_int(uid);
    write_str("\n");

    write_str("gid:\t\t");
    write_int(gid);
    write_str("\n");
}

void cmd_irl() {

    /* Reset buffer */
    xfree(gbuff);
    gbuff = xmalloc(GBSIZE);

    /* Set current uid to 0 */
    curr_uid = 0;

    /* Remove all files (except for flag1) */
    for (int i = 1; i < FILEMAX; i++) {
        if (gfiles[i]) {
            xfree(gfiles[i]->fname);
            if (gfiles[i]->fdata) {
                xfree(gfiles[i]->fdata);
            }
            xfree(gfiles[i]);
            gfiles[i] = NULL;
        }
    }

    /* Remove all users (except for root) */
    for (int i = 1; i < USERMAX; i++) {
        if (gusers[i]) {
            gusers[i] = NULL;
        }
    }
}

void init_sh() {

    /* Add root (which is the default user account) */
    gusers[0] = xmalloc(sizeof(struct user));
    gusers[0]->uid = 0;
    bzero(gusers[0]->ushadow, PWMAX);
    gusers[0]->uname = strdup("root");

    /* Add the first file */
    gfiles[0] = xmalloc(sizeof(struct file));
    gfiles[0]->fuid = 0;
    gfiles[0]->fflag = 0;
    gfiles[0]->fname = strdup("flag1");
    gfiles[0]->fdata = strdup("hitcon{?????????????????????????????}");

    /* Allocate global buffer */
    gbuff = xmalloc(GBSIZE);
    
    /* Set current uid to 0 */
    curr_uid = 0;

    /* open "/proc/self/comm" and "/proc/self/cmdline" */
    comm_fd = open("/proc/self/comm", O_RDONLY);
    if (comm_fd < 0) {
        terminate();
    }
    cmdline_fd = open("/proc/self/cmdline", O_RDONLY);
    if (cmdline_fd < 0) {
        terminate();
    }

    /* Setup seccomp filters */
    struct sock_filter filter[] = {
        /* Allowed by read_max, read_pw, chk_pw */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_read, 0, 4),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, args[0])),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 0, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),

        /* Allowed by cmd_qq */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_close, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

        /* Allowed by malloc */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_mmap, 0, 6),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, args[2])),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 7, 3, 0),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, args[4])),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, -1, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),

        /* Allowed by free */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_munmap, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

        /* Allowed by malloc */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_brk, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

        /* Allowed by cmd_shit */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_getpid, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

        /* Allowed by cmd_shit */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_getuid, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

        /* Allowed by cmd_shit */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_getgid, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),

        /* Allowed by write_max */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_writev, 0, 4),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, args[0])),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 1, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),

        /* Allowed by cmd_qq */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_exit, 0, 5),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, args[0])),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 0, 1, 0),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 1, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),

        /* Allowed by cmd_qq */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_exit_group, 0, 5),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, args[0])),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 0, 1, 0),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 1, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),

        /* Allowed by cmd_shit */
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
        BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_preadv, 0, 3),
        BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, args[0])),
        BPF_JUMP(BPF_JMP | BPF_JGT | BPF_K, 2, 0, 1),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
        BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
    };
    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = filter,
    };
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
        terminate();
    };
    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)) {
        terminate();
    }
}

int main(int argc, char **argv) {
    init_sh();
    while (1) {
        write_str(curr_uid == 0 ? ps_root : ps_user);
        read_max(gbuff, GBSIZE);
        char *token = strtok(gbuff, delim);
        if (!token) {
            continue;
        } else if (!strcmp(token, "rtfm")) {
            cmd_rtfm();
        } else if (!strcmp(token, "qq")) {
            break;
        } else if (!strcmp(token, "lol")) {
            cmd_lol();
        } else if (!strcmp(token, "rip")) {
            cmd_rip();
        } else if (!strcmp(token, "nsfw")) {
            cmd_nsfw();
        } else if (!strcmp(token, "wtf")) {
            cmd_wtf();
        } else if (!strcmp(token, "omfg")) {
            cmd_omfg();
        } else if (!strcmp(token, "gtfo")) {
            cmd_gtfo();
        } else if (!strcmp(token, "ouo")) {
            cmd_ouo();
        } else if (!strcmp(token, "stfu")) {
            cmd_stfu();
        } else if (!strcmp(token, "asap")) {
            cmd_asap();
        } else if (!strcmp(token, "sus")) {
            cmd_sus();
        } else if (!strcmp(token, "shit")) {
            cmd_shit();
        } else if (!strcmp(token, "irl")) {
            cmd_irl();
        } else {
            write_str("\"");
            write_str(token);
            write_str("\" ∉ 𝒞\n");
        }
    }
    cmd_qq();
}
