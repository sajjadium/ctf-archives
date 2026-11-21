#include "types.h"
#include "assert.h"
#include "qsort.h"

// Conversion from pointers to indices , to allow parent/child calculations
#define PTR_TO_INDEX(ptr) ((size_t) ((ptr) - (s_info->lo_)) / (s_info->size_))
#define INDEX_TO_PTR(i)   ((char*)  ((i) * (s_info->size_) + (s_info->lo_)))

// Macros for getting around in our tree
#define PARENT(ptr)  INDEX_TO_PTR((size_t) ((PTR_TO_INDEX(ptr) - 1) / 2))
#define L_CHILD(ptr) INDEX_TO_PTR(((PTR_TO_INDEX(ptr) * 2) + 1))
#define R_CHILD(ptr) INDEX_TO_PTR(((PTR_TO_INDEX(ptr) * 2) + 2))

// Data about the area to sort
typedef struct {
  char* lo_;
  char* hi_;
  size_t size_;
  int (*compar_)(const void*, const void*);
} SortInfo;

typedef struct {
  char* lo_;
  char* hi_;
} Range;

static inline void swap_elements(char* a, char* b, const size_t size)
{
  if(a == b) return;

  for(size_t i = 0; i < size; i++)
  {
    char* a_c = (char*) a + i;
    char* b_c = (char*) b + i;

    char tmp = *a_c;
    *a_c = *b_c;
    *b_c = tmp;
  }
}

// Re-Heaps a part of the heap
void siftDown(const SortInfo* const s_info, Range range)
{
  char* root = range.lo_;

  while (L_CHILD(root) <= range.hi_)
  {
    char* l_child = L_CHILD(root);
    char* r_child = R_CHILD(root);
    char* swap = root;

    if(s_info->compar_(swap, l_child) < 0)
      swap = l_child;

    if(r_child <= range.hi_ && s_info->compar_(swap, r_child) < 0)
      swap = r_child;

    if(root == swap) return;

    swap_elements(root, swap, s_info->size_);
    root = swap;
  }
}

// Heapify the entire range
void heapify(const SortInfo* const s_info)
{
  char* start = PARENT(s_info->hi_);

  while(start >= s_info->lo_)
  {
    Range range = {start, s_info->hi_};
    siftDown(s_info, range);
    start -= s_info->size_;
  }
}

// Simple heapsort
void heapsort(const SortInfo* const s_info)
{
  heapify(s_info);

  Range range = {s_info->lo_, s_info->hi_};
  while(range.hi_ > range.lo_)
  {
    swap_elements(range.hi_, range.lo_, s_info->size_);
    range.hi_ -= s_info->size_;
    siftDown(s_info, range);
  }
}

// Wrapper around heapsort
void qsort(void* ptr, size_t count, size_t size, int (*compar)(const void*, const void*))
{
  if(count == 0) return;
  if(size == 0) return;

  const SortInfo s_info = {(char*) ptr, ((char*) ptr) + (count - 1) * size, size, compar};
  heapsort(&s_info);
}
