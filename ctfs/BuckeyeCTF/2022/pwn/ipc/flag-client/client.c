#include <sys/msg.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAIN_QUEUE_KEY 1337
#define MSGTYPE_TOSERVER 1
#define MSGTYPE_TOCLIENT 2

#define SUBTYPE_SUBMIT_NOTE 3
#define SUBTYPE_GET_COUNT 2
#define SUBTYPE_PING 4
#define SUBTYPE_FLAG 5

#define SUBTYPE_REPLY_FAIL 1
#define SUBTYPE_REPLY_SUCCESS 0

#define MAX_USERMSG_BODY_SIZE 0x100
#define MAX_ALLOWED_NOTES 1000

#define SERVER_UID 1002

typedef struct favorites_s {
    struct favorites_s *next;
    char *str;
} favorite;

typedef struct main_queue_msg_s {
    long mtype;
    unsigned long sess_id;
    key_t queue_id;
} main_queue_msg;

typedef struct  {
    long mtype;
    unsigned char msubtype;
    unsigned long body_len;
    char body[];
} user_queue_msg;

int process_main_queue_msg(main_queue_msg *msg);
int process_user_queue_msg(key_t msgq, user_queue_msg *msg);

favorite *cool_notes;
unsigned long cool_notes_count;



int main() {
    int msg_queue = msgget(MAIN_QUEUE_KEY, 0);
    if (msg_queue == -1) {
        printf("msgget failed\n");
        return -1;
    }

    key_t our_key = (key_t)getpid();
    int our_queue = msgget(our_key, IPC_CREAT);
    if (our_queue == -1) {
        printf("msgget failed\n");
        return -1;
    }

    struct msqid_ds msq_config;
    msq_config.msg_perm.uid = SERVER_UID;
    msq_config.msg_perm.gid = 0;
    msq_config.msg_perm.mode = 0600;
    msq_config.msg_qbytes = 0x1000; // idk, big enough

    /* Need to grant the other process access to our queue */
    msgctl(our_queue, IPC_SET, &msq_config);

    /* Register ourselves */
    main_queue_msg msg = { 1, 0xf00d, our_queue };
    msgsnd(msg_queue, &msg, sizeof(msg), 0);

    printf("Successfully registered\n");

    // This loop services our message queue
    while (1) {
        char recvd[sizeof(user_queue_msg) + MAX_USERMSG_BODY_SIZE];
	ssize_t num_bytes = msgrcv(our_queue, recvd, sizeof(user_queue_msg) + MAX_USERMSG_BODY_SIZE, MSGTYPE_TOCLIENT, MSG_NOERROR);
        if (num_bytes > 0) {
            process_user_queue_msg(our_queue, (user_queue_msg*)recvd);
        }
    }
}

int process_user_queue_msg(key_t msgq, user_queue_msg *msg) {

    if (msg->msubtype == SUBTYPE_PING) {
        msg->mtype = MSGTYPE_TOSERVER;
        msg->body_len = 0;
        msg->msubtype = SUBTYPE_REPLY_SUCCESS;
        msgsnd(msgq, msg, sizeof(user_queue_msg), IPC_NOWAIT);
    } else if (msg->msubtype == SUBTYPE_FLAG) {
	char flagbuf[0x40];
	FILE *flagfile = fopen("/challenge/flag.txt", "r");
	int count = fread(flagbuf, 1, sizeof(flagbuf), flagfile);
	fclose(flagfile);
	
        msg->mtype = MSGTYPE_TOSERVER;
	msg->body_len = count;
	strncpy(msg->body, flagbuf, count);
	msgsnd(msgq, msg, sizeof(user_queue_msg)+sizeof(flagbuf), IPC_NOWAIT);
    }
    
    return -1;
}
