#include <linux/kernel.h>
#include <linux/syscalls.h>
#include <linux/module.h>
#include <linux/string.h>
#include <linux/fdtable.h>

#ifndef __NR_IPS
#define __NR_IPS 548
#endif

#define MAX 16

typedef struct {
  int idx;
  unsigned short priority;
  char *data;
} userdata;

typedef struct {
  void *next;
  int idx;
  unsigned short priority;
  char data[114];
} chunk;

chunk *chunks[MAX] = {NULL};
int last_allocated_idx = -1;

int get_idx(void) {
  int i;
  for(i = 0; i < MAX; i++) {
    if(chunks[i] == NULL) {
      return i;
    }
  }
  return -1;
}

int check_idx(int idx) {
  if(idx < 0 || idx >= MAX) return -1;
  return idx;
}

int remove_linked_list(int idx) {
  int i;
  for(i = 0; i < MAX; i++) {
    if(i == idx) continue;
    if(chunks[i]->next == chunks[idx]) {
      chunks[i]->next = chunks[idx]->next;
      break;
    }
  }
  return 0;
}

int alloc_storage(unsigned int priority, char *data) {
  int idx = get_idx();
  if((idx = check_idx(idx)) < 0) return -1;
  chunks[idx] = kmalloc(sizeof(chunk), GFP_KERNEL);

  if(last_allocated_idx >= 0 && !(chunks[last_allocated_idx]->next)) {
    chunks[last_allocated_idx]->next = chunks[idx];
  }

  chunks[idx]->next = NULL;
  chunks[idx]->idx = idx;
  chunks[idx]->priority = priority;
  memcpy(chunks[idx]->data, data, strlen(data));
  last_allocated_idx = idx;

  return idx;
}

int remove_storage(int idx) {
  if((idx = check_idx(idx)) < 0) return -1;
  if(chunks[idx] == NULL) return -1;

  int i;
  for(i = 0; i < MAX; i++) {
    if(i != idx && chunks[i] == chunks[idx]) {
      chunks[i] = NULL;
    }
  }

  kfree(chunks[idx]);
  chunks[idx] = NULL;

  return 0;
}

int edit_storage(int idx, char *data) {
  if((idx = check_idx(idx)) < 0);
  if(chunks[idx] == NULL) return -1;

  memcpy(chunks[idx]->data, data, strlen(data));

  return 0;
}

int copy_storage(int idx) {
  if((idx = check_idx(idx)) < 0) return -1;
  if(chunks[idx] == NULL) return -1;

  int target_idx = get_idx();
  chunks[target_idx] = chunks[idx];
  return target_idx;
}

SYSCALL_DEFINE2(ips, int, choice, userdata *, udata) {
  char data[114] = {0};
  if(udata->data && strlen(udata->data) < 115) {
    if(copy_from_user(data, udata->data, strlen(udata->data))) return -1;
  }
  switch(choice) {
    case 1: return alloc_storage(udata->priority, data);
    case 2: return remove_storage(udata->idx);
    case 3: return edit_storage(udata->idx, data);
    case 4: return copy_storage(udata->idx);
    default: return -1;
  }
}
