

#include "libzone.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>
#include <pthread.h>

#define MAX_COUNT 0x400
#define INTEGER 1
#define BUFFER  2

struct message {
    size_t id;
    size_t len;
    char * buf;
};

struct out_message {
    struct message inline_mes;
    struct out_message * next;
    bool is_cancelled_message;
};

struct task {
    struct message inline_mes;
    struct task * next;
    bool is_cancelled;
    bool is_finished;
    uint16_t timeout;
    void (*cancel_callback)(struct task *);
};

struct cmd {
    uint16_t timeout;
    uint16_t len;
    uint16_t next;
    uint16_t type;
    size_t id;
    char buf[];
};

struct task * db[MAX_COUNT];
struct task * queue_head;
struct task * queue_tail;
struct out_message * out_head;
struct out_message * out_tail;
pthread_mutex_t queue_lock;

bool kill_thread;

pthread_t tid;

int read_int() {
    char buf[20];
    memset(buf, 0, 20);
    read(0, buf, 10);
    return atoi(buf);
}

void cancel_callback_type_0(struct task * task) {
    puts("Tried to cancel a constant message");
    exit(1);
}

void cancel_callback_type_1(struct task * task) {
    task->timeout = 0;
    task->inline_mes.buf = NULL;
    task->inline_mes.len = 0;
    return 0;
}

void cancel_callback_type_2(struct task * task) {
    struct task * tmp;
    tmp = queue_head;
    while (tmp && tmp != task) {
        tmp->timeout = 0;
        tmp = tmp->next;
    }

    if (tmp == task) {
        tmp->timeout = 0;
        tmp->inline_mes.buf = NULL;
        tmp->inline_mes.len = 0;
    }
}

int find_task_in_queue(size_t id) {
    size_t i;
    for (i = (id % MAX_COUNT); i < MAX_COUNT; ++i) {
        if (db[i] && db[i]->inline_mes.id == id) {
            return i;
        }
    }
    if ((id % MAX_COUNT) > 0) {
        for (i = 0; i < (id % MAX_COUNT); ++i) {
            if (db[i] && db[i]->inline_mes.id == id) {
                return i;
            }
        }
    }
    return -1;
}



int find_free_idx(size_t id) {
    size_t i;
    for (i = (id % MAX_COUNT); i < MAX_COUNT; ++i) {
        if (db[i] == NULL) {
            return i;
        }
    }
    for (i = 0; i < (id % MAX_COUNT); ++i) {
        if (db[i] == NULL) {
            return i;
        }
    }
    return -1;
}

bool add_task_to_queue(struct task * task) {
    int idx = find_free_idx(task->inline_mes.id);
    if (idx == -1) {
        return false;
    }
    db[idx] = task;
    return true;
}

void remove_task_in_queue(size_t id) {
    size_t i;
    for (i = (id % MAX_COUNT); i < MAX_COUNT; ++i) {
        if (db[i] && db[i]->inline_mes.id == id) {
            db[i] = NULL;
            return;
        }
    }
    for (i = 0; i < (id % MAX_COUNT); ++i) {
        if (db[i] && db[i]->inline_mes.id == id) {
            db[i] = NULL;
            return;
        }
    }
}

void process_task() {
    struct task * cur_task;
    struct out_message * out;
    size_t cur_time;
    size_t start_time;
    size_t start_process = time(0);
    while ((time(0) - start_process) < 900 && !kill_thread) {

        cur_task = queue_head;
        if (cur_task != NULL) {
            
            start_time = time(0);
            while (!kill_thread) {
                cur_time = time(0);
                if (cur_task->is_cancelled) {
                    break;
                }
                if (cur_time - start_time >= cur_task->timeout) {
                    cur_task->is_finished = true;
                    break;
                }
            }
            if (kill_thread) {
                return;
            }
            pthread_mutex_lock(&queue_lock);
            remove_task_in_queue(cur_task->inline_mes.id);
            if (queue_head == queue_tail) {
                queue_head = queue_tail = NULL;
            }
            else {
                queue_head = cur_task->next;
            }
            if (cur_task->is_finished) {
                out = zone_alloc("out_message");
                out->inline_mes = cur_task->inline_mes;
                out->next = NULL;
                out->is_cancelled_message = false;

                if (out_head == NULL) {
                    out_head = out_tail = out;
                }
                else {
                    out_tail->next = out;
                    out_tail = out;
                }
            }

            zone_free("task", cur_task);
            pthread_mutex_unlock(&queue_lock);
        }
    }
}

void process_commands() {
    size_t idx;
    size_t id;
    size_t len;
    size_t n;
    size_t nb_of_cmd;
    size_t offset;
    struct object * obj;
    char * buf;
    struct cmd * pc;
    struct task * task;

    printf("Command buffer length: ");
    len = read_int();
    if (len >= 0x800) {
        puts("Buffer length too large");
        return;
    }
    if (len < sizeof(struct cmd)) {
        puts("Buffer length too small");
        return; 
    }
    buf = zmalloc(len);
    printf("Command buffer: ");
    n = read(0, buf, len);
    
    pc = (struct cmd *) buf;
    if ( (size_t)pc->len + sizeof(struct cmd) > n) {
        puts("Invalid parent command");
        goto free_resource;
    }

    if (find_task_in_queue(pc->id) >= 0) {
        puts("Task is already in queue");
        goto free_resource;
    }
    
    task = zone_alloc("task");
    task->inline_mes.id = pc->id;

    if (!add_task_to_queue(task)) {
        puts("Queue is full");
        zone_free("task", task);
        goto free_resource;
    }
    task->inline_mes.len = pc->len;
    if (pc->len) {
        task->inline_mes.buf = zmalloc(pc->len);
        memcpy(task->inline_mes.buf, pc->buf, pc->len);
    }
    else {
        task->inline_mes.buf = NULL;
    }
    task->next = NULL;
    task->timeout = pc->timeout;
    task->is_cancelled = false;
    task->is_finished = false;
    task->cancel_callback = NULL;

    switch (pc->type) {
        case 0:
            task->cancel_callback = cancel_callback_type_0;
            break;
        case 1:
            task->cancel_callback = cancel_callback_type_1;
            break;
        case 2:
            task->cancel_callback = cancel_callback_type_2;
            break;
    }

    pthread_mutex_lock(&queue_lock);
    if (queue_tail == NULL) {
        queue_head = queue_tail = task;
    }
    else {
        queue_tail->next = task;
        queue_tail = task;
    }

    pthread_mutex_unlock(&queue_lock);
    nb_of_cmd = 0;
    while (pc->next && nb_of_cmd < 5) {
        offset = pc->next;
        
        if ( (size_t)pc->len + sizeof(struct cmd) + offset > n) {
            puts("Invalid child command");
            goto free_resource;
        }

        pc = (struct cmd *) &buf[offset];
        
        task = zone_alloc("task");
        task->inline_mes.id = pc->id;
        if (!add_task_to_queue(task)) {
            puts("Queue is full");
            zone_free("task", task);
            goto free_resource;
        }
        task->inline_mes.len = pc->len;
        if (pc->len) {
            task->inline_mes.buf = zmalloc(pc->len);
            memcpy(task->inline_mes.buf, pc->buf, pc->len);
        }
        else {
            task->inline_mes.buf = NULL;
        }

        task->next = NULL;
        task->timeout = pc->timeout;
        task->is_cancelled = false;
        task->is_finished = false;

        task->cancel_callback = NULL;

        switch (pc->type) {
            case 0:
                task->cancel_callback = cancel_callback_type_0;
                break;
            case 1:
                task->cancel_callback = cancel_callback_type_1;
                break;
            case 2:
                task->cancel_callback = cancel_callback_type_2;
                break;
        }

        pthread_mutex_lock(&queue_lock);
        if (queue_tail == NULL) {
            queue_head = queue_tail = task;
        }
        else {
            queue_tail->next = task;
            queue_tail = task;
        }

        pthread_mutex_unlock(&queue_lock);  
        ++nb_of_cmd;
    }

free_resource:
    zfree(buf, len);
}

void cancel_task() {
    size_t id;
    int idx;
    struct task * task;
    struct out_message * out;

    printf("Enter Task ID: ");
    id = read_int();
    idx = find_task_in_queue(id);

    if (idx < 0) {
        puts("Task does not exist");
        return;
    }

    task = db[idx];
    pthread_mutex_lock(&queue_lock);
    if (!task->is_cancelled && !task->is_finished) {
        
        if(task->inline_mes.buf) {
            memset(task->inline_mes.buf, 0, task->inline_mes.len);
            zfree(task->inline_mes.buf, task->inline_mes.len);
        }
        task->is_cancelled = true;
        if (task->cancel_callback) {
            task->cancel_callback(task);
        }
        else {
            out = zone_alloc("out_message");
            out->inline_mes.id = task->inline_mes.id;
            out->inline_mes.buf = "CANCELLED\n";
            out->inline_mes.len = 10;
            out->next = NULL;
            out->is_cancelled_message = true;

            
            if (out_head == NULL) {
                out_head = out_tail = out;
            }
            else {
                out_tail->next = out;
                out_tail = out;
            }
            
        }
        puts("Task is cancelled");
    }
    else {
        puts("Unable to cancel task");
    }
    pthread_mutex_unlock(&queue_lock);

}
void check_message() {
    struct out_message * tmp;
    pthread_mutex_lock(&queue_lock);      
    while (out_head) {
        printf("ID 0x%llx: ", out_head->inline_mes.id);
        if (out_head->inline_mes.buf) {
            write(1, out_head->inline_mes.buf, out_head->inline_mes.len);
            printf("\n");
        }
        else {
            printf("Empty message\n");
        }
        if (!out_head->is_cancelled_message && out_head->inline_mes.buf) {
            memset(out_head->inline_mes.buf, 0, out_head->inline_mes.len);
            zfree(out_head->inline_mes.buf, out_head->inline_mes.len);
        }

        tmp = out_head;
        if (out_head == out_tail) {
            out_head = out_tail = NULL;
        }
        else {
            out_head = out_head->next;
        }
        zone_free("out_message", tmp);
    }
    pthread_mutex_unlock(&queue_lock);
}

void timeout() {
    puts("Timeout");
    exit(1);
}

void init() {
    size_t i;
    int error;
    signal(0xe,&timeout);
    alarm(900);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

    zone_create("task", sizeof (struct task));
    zone_create("out_message", sizeof (struct out_message));

    pthread_mutex_init(&queue_lock, NULL);
    error = pthread_create(&tid, NULL, &process_task, NULL);
    if (error != 0) {
        printf("Process task thread cannot be created");
        exit(1);
    }
    
}

void menu() {

    printf("\n");
    puts("------------------------");
    puts("1. Submit commands");
    puts("2. Cancel task");
    puts("3. Check message");
    puts("4. Exit");
    printf("> ");
}

int main(void) {
    init();
    puts("A terribly made notification system");
    int choice;
    while (1) {
        menu();
        choice = read_int();
        switch (choice) {
            case 1:
                process_commands();
                break;
            case 2:
                cancel_task();
                break;
            case 3:
                check_message();
                break;
            case 4:
                goto finish;
                break;
            default:
                puts("Invalid choice");
                break;
        }
    }

finish:
    kill_thread = true;
    pthread_join(tid, NULL);
    pthread_mutex_destroy(&queue_lock);
    return 0;
}