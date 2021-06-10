#include <cstdlib>
#include <cstring>
#include <unistd.h>

struct free_list {
  size_t size;
  char used;
  struct free_list *next;
  struct free_list *prev;
  void *data;
};

void *my_malloc(size_t block_size) {
  static struct free_list root = {
      .size = 0, .used = 1, .next = NULL, .prev = NULL, .data = NULL};
  block_size = block_size % sizeof(void *) == 0
                   ? block_size
                   : ((block_size / sizeof(void *)) + 1) * sizeof(void *);
  struct free_list *tmp = (&root)->next;
  struct free_list metadata = {
      .size = block_size, .used = 1, .next = NULL, .prev = NULL, .data = NULL};
  char *data;
  if (tmp == NULL) {
    data = (char *)sbrk(block_size + sizeof(struct free_list));
    if (data == (void *)-1) {
      return NULL;
    }
    metadata.prev = &root;
    metadata.data = data + sizeof(struct free_list);
    memcpy(data, &metadata, sizeof(struct free_list));
    memset(metadata.data, 0, block_size);
    root.next = (struct free_list *)data;
    return metadata.data;
  } else {
    struct free_list *prev = tmp->prev;
    while (tmp != NULL) {
      if (tmp->used == 0) {
        if (tmp->size >= block_size) {
          memset(tmp->data, 0, block_size);
          tmp->used = 1;
          return tmp->data;
        }
      }
      prev = tmp;
      tmp = tmp->next;
    }
    data = (char *)sbrk(block_size + sizeof(struct free_list));
    if (data == (void *)-1) {
      return NULL;
    }
    metadata.data = data + sizeof(struct free_list);
    memset(metadata.data, 0, block_size);
    metadata.prev = prev;
    memcpy(data, &metadata, sizeof(struct free_list));
    prev->next = (struct free_list *)data;
    return metadata.data;
  }
  return NULL;
}

void my_free(void *ptr) {
  if (ptr == NULL) {
    exit(255);
  }
  char *data = (char *)ptr;
  struct free_list *metadata =
      (struct free_list *)(data - sizeof(struct free_list));
  if (metadata->prev->used == 0) {
    struct free_list *metadata_prev = metadata->prev;
    metadata_prev->size += (metadata->size + sizeof(struct free_list));
    metadata_prev->next = metadata->next;
    if (metadata->next != NULL) {
      metadata->next->prev = metadata_prev;
    }
    metadata = metadata_prev;
  }
  metadata->used = 0;
  if (metadata->next != NULL) {
    if (metadata->next->used == 0) {
      metadata->size += (metadata->next->size + sizeof(struct free_list));
      metadata->next = metadata->next->next;
    }
  }
  if (metadata->next == NULL) {
    int size_to_decrease = metadata->size;
    size_to_decrease += (sizeof(struct free_list));
    metadata->prev->next = NULL;
    sbrk(-size_to_decrease);
  }
  return;
}
