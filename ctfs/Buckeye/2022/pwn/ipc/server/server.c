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

#define SUBTYPE_REPLY_FAIL 1
#define SUBTYPE_REPLY_SUCCESS 0

#define MAX_USERMSG_BODY_SIZE 0x100
#define MAX_ALLOWED_NOTES 1000
typedef struct session_s {
    unsigned long sess_id;
    key_t msg_queue;
    struct session_s *next;
} session;

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
int process_user_queue_msg(session *sess, user_queue_msg *msg);

session *user_queues_list;
favorite *cool_notes;
unsigned long cool_notes_count;



int main() {
    int msg_queue = msgget(MAIN_QUEUE_KEY, IPC_CREAT);
    if (msg_queue == -1) {
        printf("msgget failed\n");
        return -1;
    }

    struct msqid_ds msq_config;
    msq_config.msg_perm.uid = 0;
    msq_config.msg_perm.gid = 0;
    msq_config.msg_perm.mode = 0666; // anyone can talk to us
    msq_config.msg_qbytes = 0x1000; // idk, big enough

    /* Need to grant the other process access to our queue */
    msgctl(msg_queue, IPC_SET, &msq_config);


    // This loop services all message queues
    while (1) {
        main_queue_msg recvd;
        ssize_t num_bytes = msgrcv(msg_queue, &recvd, sizeof(main_queue_msg), 0, MSG_NOERROR|IPC_NOWAIT);
        if (num_bytes == sizeof(main_queue_msg)) {
            process_main_queue_msg(&recvd);
        }

        // Traverse all the user queues and process these messages
        session *cur = user_queues_list;
        char msg_buf[MAX_USERMSG_BODY_SIZE + sizeof(user_queue_msg)];
        while (cur != NULL) {
            int num_bytes = msgrcv(cur->msg_queue, msg_buf, sizeof(msg_buf), MSGTYPE_TOSERVER, MSG_NOERROR|IPC_NOWAIT);
            if (num_bytes > 0 && num_bytes >= sizeof(user_queue_msg) && ((user_queue_msg *)msg_buf)->body_len + sizeof(user_queue_msg) <= num_bytes) {
                process_user_queue_msg(cur, (user_queue_msg *)msg_buf);
            }
            cur = cur->next;
        }
        
        usleep(100000); // 0.1 seconds
    }
}

int process_main_queue_msg(main_queue_msg *msg) {
    switch (msg->mtype) {
        case 1: {
            session *cur = user_queues_list;
            while (cur != NULL) {
                if (cur->msg_queue == msg->queue_id) {
                    // Already in list
                    return -1;
                }
                cur = cur->next;
            }

            // Register new queue
            // (insert at beginning of linked list)
            session *new_node = malloc(sizeof(session));
	    new_node->sess_id = msg->sess_id;
	    new_node->next = user_queues_list;
            new_node->msg_queue = msg->queue_id;
            user_queues_list = new_node;
            
            printf("Registered queue: %d\n", msg->queue_id);
            break;
        }
        case 2: {
            // Deregister queue
            // (linked list removal)
            session **p2change = &user_queues_list;
            while (*p2change != NULL) {
                session *tmp = *p2change;
                if (tmp->msg_queue == msg->queue_id) {
                    *p2change = tmp->next;
                    free(tmp);
                    break;
                } else {
                    p2change = &(tmp->next);
                }
            }
            break;
            
        }
    }
    return 0;
}

int process_user_queue_msg(session *sess, user_queue_msg *msg) {
    user_queue_msg reply;
    reply.mtype = MSGTYPE_TOCLIENT;
    reply.msubtype = SUBTYPE_REPLY_FAIL;
    reply.body_len = 0;
    switch (msg->msubtype) {
        case SUBTYPE_SUBMIT_NOTE: {
            if (cool_notes_count > 1000) break;
            
            // Add new favorite
            // (insert at beginning of linked list)
            favorite *new_node = malloc(sizeof(favorite));
            new_node->next = cool_notes;
            new_node->str = malloc(msg->body_len);
            
            strcpy(new_node->str, msg->body);

            cool_notes = new_node;
            reply.msubtype = SUBTYPE_REPLY_SUCCESS;
            cool_notes_count++;
            break;
        }
        case SUBTYPE_GET_COUNT:
            reply.body_len = cool_notes_count;
            reply.msubtype = SUBTYPE_REPLY_SUCCESS;
            break;
        case SUBTYPE_PING:
            reply.msubtype = SUBTYPE_REPLY_SUCCESS;
        default:
            break;
    }

    msgsnd(sess->msg_queue, &reply, sizeof(user_queue_msg), IPC_NOWAIT);
    
    return -1;
}
