#include <sys/types.h>
#include <stdbool.h>

typedef struct chunk_metadata {
  struct chunk_metadata* next;
  size_t size;
  bool is_free;
} chunk_metadata;

typedef struct bin {
  bool rearrange;
  size_t nmemb;
  chunk_metadata* head;
} bin;

char* not_malloc(size_t size);

void not_free(char* chunk);

chunk_metadata* get_metadata(char* chunk);
