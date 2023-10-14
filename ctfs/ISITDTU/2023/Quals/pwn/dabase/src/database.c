#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <fcntl.h>
#include <poll.h>
#include <errno.h>
#include "util.h"
#include<sys/prctl.h>
#include<linux/filter.h>
#include<linux/seccomp.h>
#include <stddef.h>
#include<linux/audit.h>
#include<linux/unistd.h>
#include <string.h>


#define CL_READ_FD  0x100
#define CL_WRITE_FD 0x101

#define SYNC_CODE 0xff

#define INVALID_KEY 0xffffffffffffffff
#define MSG_GET_KEY 0x20
#define MSG_ADD_OBJ 0x21
#define MSG_GET_OBJ 0x22
#define MSG_LOAD_DB 0x23
#define MSG_SAVE_DB 0x24
#define MSG_GET_DTL 0x25

#define RES_GET_KEY 0x30
#define RES_ADD_OBJ 0x31
#define RES_GET_OBJ 0x32
#define RES_LOAD_DB 0x33
#define RES_SAVE_DB 0x34
#define RES_GET_DTL 0x35

#define SUCCESS_CODE (0)
#define FAIL_CODE (0xff00000000000000)

#define Allow(syscall) \
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_##syscall, 0, 1),\
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW)


void run_client();
void launch_client();
void install_client_seccomp();
void client_send_ready();
void database_loop();

struct sock_filter seccompfilter[]={
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, arch)),
    BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 1, 0),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
    BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
    BPF_JUMP(BPF_JMP | BPF_JGE | BPF_K, 0x40000000, 0, 1),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
    Allow(poll),
    Allow(read),
    Allow(write),
    Allow(getrandom),
    Allow(brk),
    Allow(mmap),
    Allow(mprotect),
    Allow(clock_nanosleep),
    Allow(nanosleep),
    Allow(exit),
    Allow(exit_group),
    BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL),
};

struct sock_fprog filterprog={
    .len=sizeof(seccompfilter)/sizeof(struct sock_filter),
    .filter=seccompfilter
};

uint64_t pollFd(int fd, bool block) {
    struct pollfd pfd;
    uint64_t res;
    pfd.fd = fd;
    pfd.events = POLLIN;
    pfd.revents = 0;
    if ((res = poll(&pfd, 1, block ? -1 : 0)) == -1) error("pollFd::poll failed");
    return res;
}

void sendMsg(uint64_t type, uint8_t *msg, uint64_t size) {
    uint64_t type_send = type;
    if (write(CL_WRITE_FD, &type_send, 8) != 8) error("sendMsg::write failed");
    if (msg != NULL) {
        if (write(CL_WRITE_FD, msg, size) != size) error("sendMsg::write failed");
    }
    return;
}

void recvMsgType(uint64_t *type) {
    int readSize;
    while (true) {
        pollFd(CL_READ_FD, true);
        if ((readSize = read(CL_READ_FD, type, 8)) != 8) {
        if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) error("recvMsgType::read failed");
        } 
        else {
            break;
        }
    }
}

void recvMsg(uint8_t *msg, uint64_t size) {
  int readSize = 0;
  for (uint64_t cursor = 0; cursor < size; cursor += readSize) {
    pollFd(CL_READ_FD, true);
    if ((readSize = read(CL_READ_FD, &msg[cursor], size - cursor)) <= 0) {
        if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) error("recvMsg::read failed");
        readSize = 0;
    }
  }
  return;
}
void launch_client() {
    int client_fd[2][2];
    if (pipe2(client_fd[0], O_NONBLOCK) == -1) error("launch_client::pipe2 failed");
    if (pipe2(client_fd[1], O_NONBLOCK) == -1) error("launch_client::pipe2 failed");
    pid_t pid = fork();
    if (pid < 0) error("launch_client::fork failed");
    else if (pid == 0) {
        //child
        close(client_fd[0][0]);
        close(client_fd[1][1]);
        if (dup2(client_fd[0][1], CL_WRITE_FD) == -1) error("launch_client::dup failed");
        if (dup2(client_fd[1][0], CL_READ_FD) == -1) error("launch_client::dup failed");
        close(client_fd[0][1]);
        close(client_fd[1][0]);
        run_client();
        _exit(0);
    } 
    else {
        //parent
        close(client_fd[0][1]);
        close(client_fd[1][0]);
        if (dup2(client_fd[0][0], CL_READ_FD) == -1) error("launch_client::dup failed");
        if (dup2(client_fd[1][1], CL_WRITE_FD) == -1) error("launch_client::dup failed");
        close(client_fd[0][0]);
        close(client_fd[1][1]);
        uint64_t readSize;
        uint8_t tmp = SYNC_CODE;
        if (write(CL_WRITE_FD, &tmp, 1) != 1) error("launch_client::write failed");
        while (true) {
            pollFd(CL_READ_FD, true);
            if ((readSize = read(CL_READ_FD, &tmp, 1)) != 1) {
                if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) error("launchDevice::read failed");
            } else {
                break;
            }
        }
        if (tmp != SYNC_CODE) error("launch_client::invalid sync code");
        close(STDIN_FILENO);
        close(STDOUT_FILENO);
        close(STDERR_FILENO);

        database_loop();
    }
}

void install_client_seccomp() {
    if(prctl(PR_SET_NO_NEW_PRIVS,1,0,0,0)){
        error("install_client_seccomp::PR_SET_NO_NEW_PRIVS failed");
    }
    if(prctl(PR_SET_SECCOMP,SECCOMP_MODE_FILTER,&filterprog)==-1){
        error("install_client_seccomp::PR_SET_SECCOMP failed");
    }
    return;
}

void client_send_ready() {
    uint64_t readSize;
    uint8_t tmp;
    while (true) {
        pollFd(CL_READ_FD, true);
        if ((readSize = read(CL_READ_FD, &tmp, 1)) != 1) {
        if (readSize == 0 || (errno != EWOULDBLOCK && errno != EAGAIN)) error("client_send_ready::read failed");
        } 
        else {
            break;
        }
    }
    if (tmp != SYNC_CODE) error("client_send_ready::sync code incorrect");
    if (write(CL_WRITE_FD, &tmp, 1) != 1) error("client_send_ready::write failed");
}

#define getMsgType(type) type & 0xff
#define getKey(type) (type >> 8) & 0xffff
#define getSize(type) (type >> 24) & 0xffffffffff

#define setMsgType(type) type & 0xff
#define setKey(key) ( (key & 0xffff)) << 8
#define setSize(size) ( (size & 0xffffffffff)) << 24

void client_menu() {
    puts("+----------------------------+");
    puts("| 1.  add object             |");
    puts("| 2.  get object             |");
    puts("| 3.  load database          |");
    puts("| 4.  save database          |");
    puts("| 5.  get database name      |");
    puts("| 6.  exit                   |");
    puts("+----------------------------+");
    printf("> ");
}

int get_int() {
    char buf[0x20];
    memset(buf, 0, 0x20);
    read(0, buf, 0x18);
    return atoi(buf);
}


void client_add_object() {
    uint64_t type;
    uint64_t size;
    uint64_t key;
    uint64_t res;
    char * msg;
    

    sendMsg(MSG_GET_KEY, NULL, 0);
    recvMsgType(&res);
    if (res & FAIL_CODE) {
        key = INVALID_KEY;
    }
    else {
        recvMsg(&key, 8);
    }

    if (key == INVALID_KEY) {
        puts("Database has no free key");
        return;
    }
    type |= setKey(key);
    printf("Object size: ");
    size = get_int();
    if (size >= 0x10000) {
        puts("Invalid size");
    }
    msg = malloc(size);
    type |= MSG_ADD_OBJ;
    type |= setSize(size);
    printf("Object content: ");   
    read(0, msg, size);
    
    sendMsg(type, msg, size);
    type = 0;
    recvMsgType(&res);

    if (res & FAIL_CODE) {
        puts("Failed to add object");
    }
    else {
        printf("Success! Object key is: %ld\n", key);
    }
    free(msg);
}

void client_get_object() {
    uint64_t size;
    uint64_t key;
    uint64_t type;
    uint64_t res;
    char * msg;
    
    printf("Object key: ");
    key = get_int();
    type |= setKey(key);
    printf("Object size: ");
    size = get_int();
    if (size >= 0x10000) {
        puts("Invalid size");
    }
    type |= MSG_GET_OBJ;
    type |= setSize(size);
    msg = malloc(size);
    
    sendMsg(type, NULL, 0);
    type = 0;
    recvMsgType(&res);

    if (res & FAIL_CODE) {
        puts("Failed to get object");
        free(msg);
        return;
    }

    recvMsg(msg, getSize(res));
    printf("Content: ");
    write(1, msg, getSize(res));
    puts("\n");
    free(msg);
    return;
}

void client_load_database() {
    char db_name[0x60];
    memset(db_name, 0, 0x60);
    uint64_t type;
    uint64_t res;
    printf("Database name: ");
    uint64_t size = read(0, db_name, 0x50);
    if (!size || size > 0x50) {
        error("client_load_database::read failed");
    }

    if (db_name[size - 1] == '\n') {
        db_name[size-1] = '\0';
    }
    type = MSG_LOAD_DB | setSize(size);

    sendMsg(type, db_name, size);
    type = 0;
    recvMsgType(&res);
    if (res & FAIL_CODE) {
        puts("Failed to load database");
        return;
    }

    return;
}

void client_save_database() {
    uint64_t type;
    uint64_t res;

    type = MSG_SAVE_DB;

    sendMsg(type, NULL, 0);
    type = 0;
    recvMsgType(&res);
    if (res & FAIL_CODE) {
        puts("Failed to save database");
    }
}

void client_get_db_name() {
    char db_name[0x100];
    memset(db_name, 0, 0x100);
    uint64_t type;
    uint64_t res;

    type = MSG_GET_DTL;

    sendMsg(type, NULL, 0);
    type = 0;
    recvMsgType(&res);
    if (res & FAIL_CODE) {
        puts("Failed to get database name");
        return;
    }

    recvMsg(db_name, getSize(res));
    printf("Current database name: %s\n", db_name);

}
void run_client() {
    int choice;
    install_client_seccomp();
    client_send_ready();
    
    puts("ISITDTU CTF Internal Database");
    
    while (1) {
        client_menu();
        choice = get_int();

        switch (choice) {
            case 1:
                client_add_object();
                break;
            case 2:
                client_get_object();
                break;
            case 3:
                client_load_database();
                break;
            case 4:
                client_save_database();
                break;
            case 5:
                client_get_db_name();
                break;
            default:
                puts("Goodbye!");
                _exit(0);
                break;
        }

    }

}

int get_line_int(FILE *stream) {
    int ret = -1;
    int ret_scan = fscanf(stream, "%d", &ret);
    if (ret_scan == EOF) {
        ret = EOF;
    }
    return ret;
}   

void database_loop() {
    uint64_t msgType;
    uint64_t key;
    uint64_t obj_size;
    uint64_t db_size;
    uint64_t db_name_size;
    FILE * db_stream;
    typedef struct databaseEntry {
        uint64_t size;
        uint8_t *value;
    } databaseEntry;
    databaseEntry db[0x100];
    char db_name[0x100];
    char db_path[0x100];
    char tmp_db_name[0x100];

    memset(db, 0, sizeof db);
    memset(db_name, 0, 0x100);
    memset(db_path, 0, 0x100);
    memset(tmp_db_name, 0, 0x100);
    db_size = 0x100;
    db_name_size = 4;
    strcpy(db_name, "test\0");
    db_stream = NULL;
    while (true) {
        recvMsgType(&msgType);

        switch(getMsgType(msgType)) {
            case MSG_GET_KEY:
                uint64_t free_key = INVALID_KEY;
                for (uint64_t i = 0; i < db_size; ++i) {
                    if (db[i].value == NULL) {
                        free_key = i;
                        break;
                    }
                }
                sendMsg(RES_GET_KEY | SUCCESS_CODE, &free_key, 8);
                break;
            
            case MSG_ADD_OBJ:
                key = getKey(msgType);
                obj_size = getSize(msgType);
                
                db[key].size = obj_size;
                db[key].value = calloc(obj_size, 1);
                
                if (db[key].value == NULL) {
                    sendMsg(RES_ADD_OBJ | FAIL_CODE, NULL, 0);
                    break;
                }
                recvMsg(db[key].value, obj_size);
                sendMsg(RES_ADD_OBJ | SUCCESS_CODE, NULL, 0);
                break;
            
            case MSG_GET_OBJ:
                key = getKey(msgType);
                uint64_t sz = db[key].size;
                if (sz > getSize(msgType)) {
                    sz = getSize(msgType);
                }
                if (db[key].value) {
                    sendMsg(RES_GET_OBJ | SUCCESS_CODE | setKey(key) | setSize(sz), db[key].value, sz);
                }
                else {
                    sendMsg(RES_GET_OBJ | FAIL_CODE, NULL, 0);
                }
                break;
            
            case MSG_LOAD_DB:
                uint64_t nameSize;
                nameSize = getSize(msgType);
                if (nameSize > 0x80) {
                    sendMsg(RES_LOAD_DB | FAIL_CODE, NULL, 0);
                    break;
                }
                memset(tmp_db_name, 0, 0x100);
                recvMsg(tmp_db_name, nameSize);
                bool invalidName = false;
                for (int i = 0; i < nameSize; ++i) {
                    if (!strncmp(&tmp_db_name[i], "flag", 4)) {
                        invalidName = true;
                        break;
                    }  
                    if (!strncmp(&tmp_db_name[i], "../", 3)) {
                        invalidName = true;
                        break;
                    }
                    if (tmp_db_name[i] == '\0') {
                        break;
                    }
                }

                if (invalidName) {
                    sendMsg(RES_LOAD_DB | FAIL_CODE, NULL, 0);
                    break;
                }
                
                strncpy(db_path, tmp_db_name, 0x80);

                db_stream = fopen(db_path, "r");
                if (db_stream == NULL) {
                    sendMsg(RES_LOAD_DB | FAIL_CODE, NULL, 0);
                    break;
                }

                memset(tmp_db_name, 0, 0x100);
                if (fscanf(db_stream, "%s", tmp_db_name) == EOF) {
                    sendMsg(RES_LOAD_DB | FAIL_CODE, NULL, 0);
                    fclose(db_stream);
                    db_stream = NULL;
                    break;
                }
                
                if (strlen(tmp_db_name) > 0x80) {
                    sendMsg(RES_LOAD_DB | FAIL_CODE, NULL, 0);
                    fclose(db_stream);
                    db_stream = NULL;
                    break;
                }
                db_name_size = strlen(tmp_db_name);
                strcpy(db_name, tmp_db_name);

                for (int i = 0; i < db_size; ++i) {
                    if (db[i].value) {
                        free(db[i].value);
                    }
                }

                memset(db, 0, sizeof db);
                int db_obj_size = 0;
                for (int i = 0; i < db_size; ++i) {
                    if ( (db_obj_size = get_line_int(db_stream)) != EOF) {
                        db[i].value = calloc(db_obj_size + 1, 1);
                        db[i].size = db_obj_size;
                        fscanf(db_stream, "%s", db[i].value);
                    }
                    else {
                        break;
                    }
                }

                fclose(db_stream);
                db_stream = NULL;
                sendMsg(RES_LOAD_DB | SUCCESS_CODE, NULL, 0);
                break;
            
            case MSG_SAVE_DB:
                strncpy(db_path, db_name, 0x80);
                db_stream = fopen(db_path, "w");
                if (db_stream == NULL) {
                    sendMsg(RES_SAVE_DB | FAIL_CODE, NULL, 0);
                    break;
                }

                fprintf(db_stream, "%s\n", db_name);
                
                for (int i = 0; i < db_size; ++i) {
                    if (db[i].value) {
                        fprintf(db_stream, "%d\n", db[i].size);
                        fprintf(db_stream, "%s\n", db[i].value);
                    }
                }

                sendMsg(RES_SAVE_DB | SUCCESS_CODE, NULL, 0);
                fclose(db_stream);
                break;

            case MSG_GET_DTL:
                sendMsg(RES_GET_DTL| SUCCESS_CODE | setSize(db_name_size), db_name, db_name_size);
                break;
        }

    }

}

void timeout() {
    puts("Timeout");
    exit(1);
}

int main(void) {
    
    signal(0xe,&timeout);
    alarm(120);

    if (chdir("./db")) {
        error("main::chdir failed");
    }
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    launch_client();
    
}