#ifndef KERNEL_DRIVER_UAF_SHIELD_INTERNAL_H_
#define KERNEL_DRIVER_UAF_SHIELD_INTERNAL_H_
#include <linux/kernel.h>
#include <linux/module.h>

#define log(msg, ...) printk(KERN_INFO "[" DEV "] " msg "\n", ##__VA_ARGS__)
#define err(msg, ...) \
  printk(KERN_ALERT "[" DEV "] error: " msg "\n", ##__VA_ARGS__)

#define RET_ASSERT(cond)                    \
  do {                                      \
    if (!(cond)) {                          \
      err("assertion '" #cond "' failed."); \
      return -EINVAL;                       \
    }                                       \
  } while (0)

typedef union {
  struct {
    uint64_t rsv1 : 9;
    uint64_t lsb_2 : 2;
    uint64_t r_hlat : 1;
    uint64_t rsv2 : 40;
    uint64_t msb_7 : 7;
    uint64_t rsv3 : 5;
  };
  pud_t value;
} pdpte_t;

typedef struct {
  pid_t pid;  // this is the key!
  struct mm_struct* mm;
  uint64_t num_of_tags;
  uint64_t orig_pgd_index;
  uint64_t orig_p4d_index;
  unsigned int shield;
  struct kref refcount;
  struct hlist_node node;
  struct list_head P4D_Head_Node;
  struct list_head PUD_Head_Node;
} h_node;

typedef struct {
  struct list_head list;
  p4d_t* ptr_p4d;
  pgd_t* ptr_pgd;
} list_p4d;

typedef struct {
  struct list_head list;
  pud_t* ptr;
} list_pud;

typedef struct _PTE {
  unsigned long v : 1;     /* Entry is valid */
  unsigned long vsid : 24; /* Virtual segment identifier */
  unsigned long h : 1;     /* Hash algorithm indicator */
  unsigned long api : 6;   /* Abbreviated page index */
  unsigned long rpn : 20;  /* Real (physical) page number */
  unsigned long : 3;       /* Unused */
  unsigned long r : 1;     /* Referenced */
  unsigned long c : 1;     /* Changed */
  unsigned long w : 1;     /* Write-thru cache mode */
  unsigned long i : 1;     /* Cache inhibited */
  unsigned long m : 1;     /* Memory coherence */
  unsigned long g : 1;     /* Guarded */
  unsigned long : 1;       /* Unused */
  unsigned long pp : 2;    /* Page protection */
} PTE;

#endif  // KERNEL_DRIVER_UAF_SHIELD_INTERNAL_H_
