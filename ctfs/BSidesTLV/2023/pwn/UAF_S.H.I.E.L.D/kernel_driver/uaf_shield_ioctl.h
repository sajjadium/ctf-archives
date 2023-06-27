#include <linux/ioctl.h>

#define DEV "UAF S.H.I.E.L.D"
#define PAGE_TABLE_IOCTL_MAGIC 'L'
#define IOCTL_ALLOC_PTR _IOWR(PAGE_TABLE_IOCTL_MAGIC, 3, alloc_ptr_t)
#define IOCTL_FREE_PTR _IOWR(PAGE_TABLE_IOCTL_MAGIC, 4, alloc_ptr_t)

typedef struct {
  uint64_t virt_in;
  uint64_t alloc_size;
  uint64_t virt_out;
} alloc_ptr_t;

typedef struct {
  uint64_t virt_in;
  uint64_t virt_out;
} free_ptr_t;

typedef union {
  struct {
    uint64_t pud_index : 9;
    uint64_t p4d_index : 9;
    uint64_t pgd_index : 8;
  };
  uint64_t value;
} counter_t;
