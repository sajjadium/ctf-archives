#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdbool.h>
#include "notmalloc.h"
#include <math.h>
#include <string.h>

#define MIN_HEAP_SIZE 0x4000
#define ALLOCATOR_SIGNATURE_SIZE 0x10
#define ALLOCATOR_VERSION_SIZE 0x10
#define QUICK_BIN_MAX 0x180
#define UNIT_SIZE 0x20

// contains user data
void* data_heap;

// contains metadata used by the allocator
void* metadata_heap;

// wilderness
char* top_chunk;

// bin for big chunks, split-able and consolidate-able
bin misc_bin;

// bins for small chunks that cannot be split nor consolidated
bin quick_bins[QUICK_BIN_MAX/UNIT_SIZE-1];

// allocator info
char allocator_signature[ALLOCATOR_SIGNATURE_SIZE];
char allocator_version[ALLOCATOR_VERSION_SIZE];

// get some memory pages
void* get_mapping(void* addr, int flags,size_t size){
  void* addr_ = mmap(addr,size,PROT_READ | PROT_WRITE,flags,-1,0);
  if (addr_ == MAP_FAILED) {
    puts("mmap error");
    exit(1);
  }
  return addr_;
}

// extend fixed pages
void extend_mapping(void* addr,size_t size) {
  get_mapping(addr,MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, size);
} 

// setup
void __attribute__((constructor)) setup(){
  setbuf(stdin,NULL);
  setbuf(stdout,NULL);
  setbuf(stderr,NULL);

  size_t heap_size = 0;
  printf("HEAP SIZE > ");
  scanf("%zx%*c",&heap_size);
  if(heap_size < MIN_HEAP_SIZE) {
    printf("please pick a heap size >= 0x%zx\n",MIN_HEAP_SIZE);
    exit(1);
  }
  metadata_heap = get_mapping(NULL,MAP_PRIVATE | MAP_ANONYMOUS,heap_size);
  data_heap = get_mapping(NULL,MAP_PRIVATE | MAP_ANONYMOUS,heap_size);
  //reduce size by half for non-pro clients
  data_heap += heap_size/2;

  for(bin* qb = quick_bins ; qb < quick_bins + QUICK_BIN_MAX/UNIT_SIZE-1 ; ++qb){
    qb->nmemb = 0;
    qb->head = NULL;
    qb->rearrange = false;
  }

  misc_bin.nmemb = 0;
  misc_bin.head = NULL;
  misc_bin.rearrange = true;

  top_chunk = data_heap;

  chunk_metadata* top_metadata = (chunk_metadata*)metadata_heap;
  top_metadata->size = heap_size/2;
  top_metadata->is_free = true;
  top_metadata->next = NULL;

  char** allocator_info = (char**)not_malloc(sizeof(char *)*2);
  *allocator_info = allocator_signature;
  allocator_info[1] = allocator_version;
  strcpy(allocator_signature,"not-malloc-free");
  strcpy(allocator_version,"1.3.37");
  printf("Thank you for choosing %s for your allocations needs !\nVersion %s\nSubscribe to pro to disable this automatic message.\n\n",*allocator_info,allocator_info[1]);
}

chunk_metadata* get_metadata(char* chunk){
  return (chunk_metadata*)(chunk + (long long) (metadata_heap - data_heap));
}

char* get_chunk(chunk_metadata* metadata){
  return (char*)metadata - (long long) (metadata_heap - data_heap);
}

chunk_metadata* split_chunk(chunk_metadata* metadata,size_t size) {
  size_t old_size = metadata->size;

  metadata->size = size;

  chunk_metadata* down_meta = (chunk_metadata*)((char*)metadata + metadata->size);
  down_meta->size = old_size - size;
  down_meta->next = metadata->next;

  return down_meta;
}

// remove of split chunk from free_list
char* unlink_(chunk_metadata* curr, chunk_metadata* prev, size_t size, bin* free_list) {
  // quick bins chunks are already considered not free
  if(free_list->rearrange) {
    curr->is_free = false;
  }

  //split chunk if big enough
  if(free_list->rearrange && (curr->size - UNIT_SIZE >= size)) {
    chunk_metadata* rem_meta = split_chunk(curr,size);
    rem_meta->is_free = free_list->rearrange;
    if(prev) {
      prev->next = rem_meta;
    } else {
      free_list->head = rem_meta;
    }

  // or simply remove it
  } else {
    if(prev) {
      prev->next = curr->next;
    } else {
      free_list->head = free_list->head->next;
    }
    free_list->nmemb -= 1;
  }

  return get_chunk(curr);
}

// try grabbing a chunk of size size from free_list
char* get_free_chunk(size_t size,bin* free_list) {
  if(!free_list->head || !free_list->nmemb) {
    return NULL;
  }

  chunk_metadata* prev = NULL;
  chunk_metadata* curr = free_list->head;

  for(int i = 0 ; curr && i < free_list->nmemb ; ++i) {
    // quick bins always pass check since it must be of correct size
    if ((curr->size >= size) || !free_list->rearrange) {
      return unlink_(curr,prev,size,free_list);
    }
    prev = curr;
    curr = curr->next;
  }

  return NULL;
}

// get a chunk of size size
char* not_malloc(size_t size) {
  if(!size) return NULL;
  size_t rem = size % UNIT_SIZE;
  if(rem) {
    size += UNIT_SIZE - rem;
  }

  // try reusing a freed chunk
  char* chunk = NULL;
  if (size < QUICK_BIN_MAX) {
    chunk = get_free_chunk(size,&(quick_bins[size/UNIT_SIZE-1]));
  }
  if(!chunk) {
    chunk = get_free_chunk(size,&misc_bin);
  }

  // otherwise allocate from top
  if(!chunk){
    // allocating from top chunk, extending memory mappings if necessary
    chunk = top_chunk;
    chunk_metadata* metadata = get_metadata(chunk);
    if(size > metadata->size - UNIT_SIZE){
      size_t new_size = ((size + UNIT_SIZE) & ~(size_t)0xfff) + 0x1000;
      extend_mapping((void*)((size_t)top_chunk & ~(size_t)0xfff),new_size);
      extend_mapping((void*)((size_t)metadata & ~(size_t)0xfff),new_size);
      metadata->size = new_size - ((size_t)top_chunk & (size_t)0xfff);
    }

    //set new & top chunks metadatas
    top_chunk += size;

    chunk_metadata* top_metadata = (chunk_metadata*)((char*)metadata+size);
    top_metadata->size = metadata->size - size;
    top_metadata->is_free = true;
    top_metadata->next = NULL;

    metadata->size = size;
    metadata->is_free = false;
  }

  return chunk;
}

// try consolidating chunk with the chunk directly above it
bool backward_consolidate(char* chunk, bin* free_list) {
  if(!free_list->head) return false;

  chunk_metadata* metadata = get_metadata(chunk);

  chunk_metadata* curr = free_list->head;
  for(int i = 0 ; (i < free_list->nmemb) && curr ; ++i) {
    if(chunk == get_chunk(curr) + curr->size) {
      curr->size += metadata->size;
      return true;
    }
    curr = curr->next;
  }
  return false;
}

// try consolidating chunk with the chunk directly below it
void forward_consolidate(char* chunk, bin* free_list) {
  chunk_metadata* metadata = get_metadata(chunk);
  chunk_metadata* down_meta = (chunk_metadata*)((char*)metadata+metadata->size);

  if(chunk + metadata->size == top_chunk){
    top_chunk = chunk;
    metadata->size += down_meta->size;
    metadata->is_free = true;
    return;
  }

  if(down_meta->is_free){
    metadata->size += down_meta->size;

    if(!free_list->head) return;

    chunk_metadata* prev = free_list->head;
    chunk_metadata* curr = prev->next;
    for(int i = 0 ; (i < free_list->nmemb) && curr ; ++i) {
      if(curr == down_meta) {
        prev->next = curr->next;
        free_list->nmemb -= 1;
        return;
      }

      prev = curr;
      curr = prev->next;
    }
  }
}

// add chunk to free_list
void link_(char* chunk, bin* free_list) {
  if (!chunk) return;
  if(free_list->rearrange){
    forward_consolidate(chunk,free_list);
    if(top_chunk == chunk) return;
    if (backward_consolidate(chunk,free_list)) return;
  }

  chunk_metadata* metadata = get_metadata(chunk);
  metadata->is_free = free_list->rearrange;
  metadata->next = free_list->head;
  free_list->head = metadata;
  free_list->nmemb +=1;
}

// free chunk
void not_free(char* chunk){
  size_t size = get_metadata(chunk)->size;
  if(!size || (size % UNIT_SIZE)) {
    puts("corrupted chunk size");
    exit(1);
  }
  if(size >= QUICK_BIN_MAX) {
    link_(chunk,&misc_bin);
  } else {
    link_(chunk,&(quick_bins[get_metadata(chunk)->size/UNIT_SIZE-1]));
  }
}
