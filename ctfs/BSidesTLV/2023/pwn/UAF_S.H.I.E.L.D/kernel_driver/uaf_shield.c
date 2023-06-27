#include <asm/pgalloc.h>
#include <asm/pgtable_64.h>
#include <asm/special_insns.h>
#include <linux/fs.h>
#include <linux/hashtable.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/mm.h>
#include <linux/mm_types.h>
#include <linux/module.h>
#include <linux/random.h>
#include <linux/sched/mm.h>
#include <linux/slab.h>

#include "uaf_shield_internal.h"
#include "uaf_shield_ioctl.h"

#define TAG_BITS_NUM (14)
#define MAX_PTR_NUM (1ull << TAG_BITS_NUM)
#define MAX_PTR_MASK (MAX_PTR_NUM - 1)
#define MASK_PUD ((1ull << PUD_SHIFT) - 1)
#define BIT_IN_BYTE (8)
#define MAX_USER_SPACE ((1ull << (PGDIR_SHIFT + 8)) - 1)
#define MASK_BITS(n) ((1ull << (n)) - 1)
#define MAX_TRYS (0x10)
#define MAX_ENTRYS (0x03)
#define MARKER (0x1FF)
#define CONTINUE (0)
#define LAST_PAGE (0)
#define DEBUG_PRINT (0)

DECLARE_HASHTABLE(tbl, 10);
uint64_t p4d_alloc_counter;
uint64_t pud_alloc_counter;
spinlock_t open_lock;
spinlock_t release_lock;
typedef long (*ioctl_t)(struct file *filep, unsigned int cmd,
                        unsigned long arg);
h_node *get_current_node(pid_t pid);

static inline p4d_t *_p4d_alloc_one(struct mm_struct *mm, unsigned long addr) {
  gfp_t gfp = GFP_KERNEL_ACCOUNT;

  return (p4d_t *)get_zeroed_page(gfp);
}

static inline pud_t *_pud_alloc_one(struct mm_struct *mm, unsigned long addr) {
  gfp_t gfp = GFP_PGTABLE_USER;

  return (pud_t *)get_zeroed_page(gfp);
}

int __p4d_alloc(struct mm_struct *mm, pgd_t *pgd, unsigned long address) {
  p4d_t *new = _p4d_alloc_one(mm, address);

  if (!new) return -ENOMEM;

  // spin_lock(&mm->page_table_lock);
  if (pgd_present(*pgd)) { /* Another has populated it */
    p4d_free(mm, new);
  } else {
    smp_wmb(); /* See comment in __pte_alloc */
    pgd_populate(mm, pgd, new);
  }
  // spin_unlock(&mm->page_table_lock);
  return 0;
}

int __pud_alloc(struct mm_struct *mm, p4d_t *p4d, unsigned long address) {
  pud_t *new = _pud_alloc_one(mm, address);

  if (!new) return -ENOMEM;

  // spin_lock(&mm->page_table_lock);
  if (!p4d_present(*p4d)) {
    mm_inc_nr_puds(mm);
    smp_wmb(); /* See comment in __pte_alloc */
    p4d_populate(mm, p4d, new);
  } else /* Another has populated it */
    pud_free(mm, new);
  // spin_unlock(&mm->page_table_lock);
  return 0;
}

pud_t *get_pud(struct mm_struct *mm, uint64_t addr) {
  pgd_t *t_pgd = NULL;
  p4d_t *t_p4d = NULL;
  pud_t *t_pud = NULL;
  // get original pud entry
  t_pgd = pgd_offset(mm, addr);
  if (pgd_none(*t_pgd) || !pgd_present(*t_pgd)) {
#if DEBUG_PRINT
    pr_info("pgd_offset fail. t_pgd=%llx\n", (uint64_t)t_pgd);
#endif
    return NULL;
  }
  t_p4d = p4d_offset(t_pgd, addr);
  if (p4d_none(*t_p4d) || !p4d_present(*t_p4d)) {
#if DEBUG_PRINT
    pr_info("p4d_offset fail. t_p4d=%llx\n", (uint64_t)t_p4d);
#endif
    return NULL;
  }
  t_pud = pud_offset(t_p4d, addr);
  if (pud_none(*t_pud) || !pud_present(*t_pud)) {
#if DEBUG_PRINT
    pr_info("pud_offset fail. t_pud=%llx\n", (uint64_t)t_pud);
#endif
    return NULL;
  }
  return t_pud;
}

pgd_t __pti_set_user_pgtbl(pgd_t *pgdp, pgd_t pgd) {
  /*
   * Changes to the high (kernel) portion of the kernelmode page
   * tables are not automatically propagated to the usermode tables.
   *
   * Users should keep in mind that, unlike the kernelmode tables,
   * there is no vmalloc_fault equivalent for the usermode tables.
   * Top-level entries added to init_mm's usermode pgd after boot
   * will not be automatically propagated to other mms.
   */
  if (!pgdp_maps_userspace(pgdp)) return pgd;

  /*
   * The user page tables get the full PGD, accessible from
   * userspace:
   */
  kernel_to_user_pgdp(pgdp)->pgd = pgd.pgd;

  /*
   * If this is normal user memory, make it NX in the kernel
   * pagetables so that, if we somehow screw up and return to
   * usermode with the kernel CR3 loaded, we'll get a page fault
   * instead of allowing user code to execute with the wrong CR3.
   *
   * As exceptions, we don't set NX if:
   *  - _PAGE_USER is not set.  This could be an executable
   *     EFI runtime mapping or something similar, and the kernel
   *     may execute from it
   *  - we don't have NX support
   *  - we're clearing the PGD (i.e. the new pgd is not present).
   */
  if ((pgd.pgd & (_PAGE_USER | _PAGE_PRESENT)) ==
          (_PAGE_USER | _PAGE_PRESENT) &&
      (__supported_pte_mask & _PAGE_NX))
    pgd.pgd |= _PAGE_NX;

  /* return the copy of the PGD we want the kernel to use: */
  return pgd;
}

void data_release(struct kref *ref) {
  h_node *data = container_of(ref, h_node, refcount);

  kfree(data);
}

h_node *get_current_node(pid_t pid) {
  h_node *cur = NULL;

  // Get the element with pid.
  hash_for_each_possible(tbl, cur, node, pid) {
    // Check if pid exist.
    if (cur->pid == pid) {
      kref_get(&cur->refcount);
      break;
    }
  }
  return cur;
}

int add_node_p4d(p4d_t *ptr_p4d, pgd_t *ptr_pgd, h_node *cur) {
  list_p4d *temp_node = NULL;

  /*Creating Node*/
  temp_node = kmalloc(sizeof(list_p4d), GFP_KERNEL);
  if (!temp_node) {
    p4d_free(cur->mm, ptr_p4d);
    native_pgd_clear(ptr_pgd);
    return -ENOMEM;
  }
#if DEBUG_PRINT
  pr_info("alloc p4d\n");
#endif
  p4d_alloc_counter += 1;
  /*Assgin the data that is received*/
  temp_node->ptr_p4d =
      (p4d_t *)((uint64_t)ptr_p4d & ~((uint64_t)(PAGE_SIZE - 1)));
  temp_node->ptr_pgd = ptr_pgd;
  /*Init the list within the struct*/
  INIT_LIST_HEAD(&temp_node->list);
  /*Add Node to Linked List*/
  list_add_tail(&temp_node->list, &cur->P4D_Head_Node);
  return 0;
}

int add_node_pud(pud_t *ptr, h_node *cur) {
  list_pud *temp_node = NULL;

  /*Creating Node*/
  temp_node = kmalloc(sizeof(list_pud), GFP_KERNEL);
  if (!temp_node) {
    pud_free(cur->mm, ptr);
    return -ENOMEM;
  }
#if DEBUG_PRINT
  pr_info("alloc pud\n");
#endif
  pud_alloc_counter += 1;
  /*Assgin the data that is received*/
  temp_node->ptr = (pud_t *)((uint64_t)ptr & ~((uint64_t)(PAGE_SIZE - 1)));
  /*Init the list within the struct*/
  INIT_LIST_HEAD(&temp_node->list);
  /*Add Node to Linked List*/
  list_add_tail(&temp_node->list, &cur->PUD_Head_Node);
  return 0;
}

unsigned int generate_shield(unsigned int *shield) {
  *shield = *shield * 0xbeef + 0xdead + 0xdead;
  return *shield & MAX_PTR_MASK;
}

long alloc_ptr(struct file *filep, unsigned int cmd, unsigned long arg) {
  alloc_ptr_t *alloc_arg = (alloc_ptr_t *)arg;
  pgd_t *pgd = NULL;
  p4d_t *p4d = NULL;
  pud_t *pud = NULL;
  pud_t *t_pud = NULL;
  pdpte_t tmp_pdpte = {0};
  uint64_t addr = 0;
  uint64_t _pud_index = 0;
  counter_t tmp_count = {0};
  uint64_t number_of_entrys = 0;
  uint64_t try = 0;
  uint64_t entry_num = 0;
  uint64_t index = 0;
  pdpte_t source_puds[MAX_ENTRYS] = {0};
  pud_t *dest_puds[MAX_ENTRYS] = {0};
  h_node *cur = NULL;

  if (__builtin_add_overflow(alloc_arg->virt_in, alloc_arg->alloc_size,
                             &addr) ||
      alloc_arg->alloc_size == 0 ||
      !access_ok((void *)alloc_arg->virt_in, alloc_arg->alloc_size)) {
    goto fail;
  }

  cur = get_current_node(current->pid);

  if (cur == NULL) {
    // object not found
    goto fail;
  }

  spin_lock(&cur->mm->page_table_lock);
  if (cur->orig_pgd_index != pgd_index(alloc_arg->virt_in) ||
      cur->orig_p4d_index != p4d_index(alloc_arg->virt_in)) {
    goto fail;
  }

  number_of_entrys = (((addr - 1) - (alloc_arg->virt_in)) >> PUD_SHIFT) + 1;
  if ((number_of_entrys > MAX_ENTRYS) ||
      (cur->num_of_tags > ((MAX_PTR_NUM / 2) - number_of_entrys)))
    goto fail;

  for (entry_num = 0; entry_num < number_of_entrys; entry_num++) {
    t_pud = get_pud(cur->mm,
                    alloc_arg->virt_in + (entry_num * (1ull << PUD_SHIFT)));
    if (t_pud == NULL) break;

    source_puds[try++].value = *t_pud;
  }

  if (entry_num != number_of_entrys) goto fail;

  for (try = 0; try < MAX_TRYS; try++) {
    tmp_count.value = generate_shield(&cur->shield);
    if (tmp_count.pgd_index == cur->orig_pgd_index &&
        tmp_count.p4d_index == cur->orig_p4d_index)
      continue;

    for (index = 0; index < number_of_entrys; index++) {
      addr = (tmp_count.value + index) << PUD_SHIFT;
      pgd = pgd_offset(cur->mm, addr);

      if (pgd_none(*pgd)) {
        p4d = p4d_alloc(cur->mm, pgd, addr);
        if (!p4d || add_node_p4d(p4d, pgd, cur)) {
          goto fail;
        }
      } else {
        p4d = p4d_offset(pgd, addr);
      }

      if (p4d_none(*p4d)) {
        pud = pud_alloc(cur->mm, p4d, addr);
        if (!pud || add_node_pud(pud, cur)) {
          goto fail;
        }
      } else {
        pud = pud_offset(p4d, addr);
      }
      dest_puds[index] = pud;
      if (!pud_none(*pud)) break;
    }

    if (index == number_of_entrys) break;
  }

  if (try == MAX_TRYS) {
    goto fail;
  }

  for (try = 0; try < number_of_entrys; try++) {
    t_pud = dest_puds[try];
    // TODO: check if need to remove
    if (t_pud == NULL) break;

    tmp_pdpte.value = source_puds[try].value;
    if (try == 0) {
      _pud_index = pud_index(alloc_arg->virt_in);
      tmp_pdpte.lsb_2 = _pud_index & MASK_BITS(2);
      tmp_pdpte.msb_7 = (_pud_index >> 2) & MASK_BITS(7);
    }

    if (try == number_of_entrys - 1) {
      // TODO:find a better bit
      tmp_pdpte.r_hlat = LAST_PAGE;
    } else {
      // TODO:find a better bit
      tmp_pdpte.r_hlat = CONTINUE;
    }
    native_set_pud(t_pud, tmp_pdpte.value);
  }

  if (try != number_of_entrys) {
    goto fail;
  }

  cur->num_of_tags += number_of_entrys;
  spin_unlock(&cur->mm->page_table_lock);
  alloc_arg->virt_out =
      (tmp_count.value << PUD_SHIFT) | (alloc_arg->virt_in & MASK_PUD);
  kref_put(&cur->refcount, data_release);
  return 0;

fail:
  if (cur) {
    spin_unlock(&cur->mm->page_table_lock);
    kref_put(&cur->refcount, data_release);
  }
  return -EINVAL;
}

long free_ptr(struct file *filep, unsigned int cmd, unsigned long arg) {
  free_ptr_t *alloc_arg = (free_ptr_t *)arg;
  pdpte_t tmp_pdpte = {0};
  counter_t tmp_count = {0};
  pgd_t *t_pgd = NULL;
  pud_t *t_pud = NULL;
  pud_t *t_puds[MAX_ENTRYS] = {0};
  uint64_t entry_num = 0;
  uint64_t index = 0;
  uint64_t addr = 0;
  h_node *cur = get_current_node(current->pid);

  if (cur == NULL) {
    // object not found
    goto fail;
  }

  if (alloc_arg->virt_in == (uint64_t)NULL) {
    alloc_arg->virt_out = 0;
    kref_put(&cur->refcount, data_release);
    return 0;
  }

  spin_lock(&cur->mm->page_table_lock);
  t_pgd = cur->mm->pgd;

  if (t_pgd == NULL || cur->num_of_tags == 0 ||
      alloc_arg->virt_in > MAX_USER_SPACE)
    goto fail;

  for (entry_num = 0; entry_num < MAX_ENTRYS; entry_num++) {
    addr = alloc_arg->virt_in + (entry_num * (1ull << PUD_SHIFT));
    t_pud = get_pud(cur->mm, addr);
    if (t_pud == NULL) break;

    t_puds[entry_num] = t_pud;
    tmp_pdpte.value = *t_pud;
    if (tmp_pdpte.r_hlat == LAST_PAGE) break;
  }

  if (t_pud == NULL || entry_num == MAX_ENTRYS) goto fail;

  tmp_pdpte.value = *t_puds[0];
  for (index = 0; index < entry_num + 1; index++) {
    native_pud_clear(t_puds[index]);
  }

  cur->num_of_tags -= (entry_num + 1);
  spin_unlock(&cur->mm->page_table_lock);
  asm volatile("invlpg (%0)" ::"r"(alloc_arg->virt_in) : "memory");
  /*restore original virtual address*/
  tmp_count.pud_index = (tmp_pdpte.msb_7 << 2) | tmp_pdpte.lsb_2;
  tmp_count.p4d_index = cur->orig_p4d_index;
  tmp_count.pgd_index = cur->orig_pgd_index;
  alloc_arg->virt_out =
      (tmp_count.value << PUD_SHIFT) | (alloc_arg->virt_in & MASK_PUD);
  kref_put(&cur->refcount, data_release);

  return 0;

fail:
  if (cur) {
    spin_unlock(&cur->mm->page_table_lock);
    kref_put(&cur->refcount, data_release);
  }
  return -EINVAL;
}

long step_ioctl(struct file *filep, unsigned int cmd, unsigned long arg) {
  char data[256];
  ioctl_t handler = NULL;
  long ret;

  switch (cmd) {
    case IOCTL_ALLOC_PTR:
      handler = alloc_ptr;
      break;
    case IOCTL_FREE_PTR:
      handler = free_ptr;
      break;
    default:
      return -EINVAL;
  }

  RET_ASSERT(handler && (_IOC_SIZE(cmd) < 256));
  if (copy_from_user(data, (void __user *)arg, _IOC_SIZE(cmd))) return -EFAULT;

  ret = handler(filep, cmd, (unsigned long)((void *)data));

  if (!ret && (cmd & IOC_OUT)) {
    if (copy_to_user((void __user *)arg, data, _IOC_SIZE(cmd))) return -EFAULT;
  }

  return 0;
}

int step_open(struct inode *inode, struct file *file) {
  h_node *cur = NULL;
  pid_t c_pid = current->pid;
#if DEBUG_PRINT
  pr_info("device open, pid=%llx\n", (uint64_t)c_pid);
#endif
  spin_lock(&open_lock);
  // Get the element with pid.
  hash_for_each_possible(tbl, cur, node, c_pid) {
    // Check if pid exist.
    if (cur->pid == c_pid) {
      spin_unlock(&open_lock);
      return -EBUSY;
    }
  }

  cur = NULL;
  cur = kmalloc(sizeof(h_node), GFP_KERNEL);
  if (!cur) {
    spin_unlock(&open_lock);
    return -ENOMEM;
  }

  kref_init(&cur->refcount);
  cur->pid = c_pid;
  cur->mm = current->mm;
  mmgrab(cur->mm);
  cur->num_of_tags = 0;
  cur->shield = 0x58ba82a0;
  cur->orig_pgd_index = pgd_index(cur->mm->brk);
  cur->orig_p4d_index = p4d_index(cur->mm->brk);
  INIT_LIST_HEAD(&cur->P4D_Head_Node);
  INIT_LIST_HEAD(&cur->PUD_Head_Node);

  // Insert the elements.
  hash_add(tbl, &cur->node, cur->pid);
  spin_unlock(&open_lock);
  return 0;
}

int step_release(struct inode *inode, struct file *file) {
  h_node *cur = NULL;
  list_p4d *cursor_p4d, *temp_p4d;
  list_pud *cursor_pud, *temp_pud;
  pid_t c_pid = current->pid;
#if DEBUG_PRINT
  pr_info("device close, pid=%llx\n", (uint64_t)c_pid);
  pr_info("p4d alloc in close: %lld\n", p4d_alloc_counter);
  pr_info("pud alloc in close: %lld\n", pud_alloc_counter);
#endif

  spin_lock(&release_lock);

  cur = get_current_node(c_pid);
  if (cur == NULL) {
    // object not found
    return -EINVAL;
  }

  /*free all page tables*/
  spin_lock(&cur->mm->page_table_lock);
  list_for_each_entry_safe(cursor_pud, temp_pud, &cur->PUD_Head_Node, list) {
    pud_free(cur->mm, cursor_pud->ptr);
    pud_alloc_counter -= 1;
    mm_dec_nr_puds(cur->mm);
    list_del(&cursor_pud->list);
    kfree(cursor_pud);
  }

  list_for_each_entry_safe(cursor_p4d, temp_p4d, &cur->P4D_Head_Node, list) {
    p4d_free(cur->mm, cursor_p4d->ptr_p4d);
    p4d_alloc_counter -= 1;
    native_pgd_clear(cursor_p4d->ptr_pgd);
    list_del(&cursor_p4d->list);
    kfree(cursor_p4d);
  }
  spin_unlock(&cur->mm->page_table_lock);
  mmdrop(cur->mm);
#if DEBUG_PRINT
  pr_info("p4d after free in close: %lld\n", p4d_alloc_counter);
  pr_info("pud after free in close: %lld\n", pud_alloc_counter);
#endif

  // Get the element with pid.
  hash_for_each_possible(tbl, cur, node, c_pid) {
    // Check if pid exist.
    if (cur->pid == c_pid) {
      // Remove elements.
      hash_del(&cur->node);
      kref_put(&cur->refcount, data_release);
      break;
    }
  }
  spin_unlock(&release_lock);
  return 0;
}

static const struct file_operations step_fops = {.owner = THIS_MODULE,
                                                 .compat_ioctl = step_ioctl,
                                                 .unlocked_ioctl = step_ioctl,
                                                 .open = step_open,
                                                 .release = step_release};

static struct miscdevice step_dev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = DEV,
    .fops = &step_fops,
    .mode = 0666  // S_IRUGO | S_IWUGO
};

static int __init uaf_init(void) {
  uint64_t cr4 = __read_cr4();
  p4d_alloc_counter = 0;
  pud_alloc_counter = 0;

  if (!(cr4 & (1UL << 12UL))) {
    return -EINVAL;
  }
  /* Register virtual device */
  if (misc_register(&step_dev)) {
    err("virtual device registration failed..");
    step_dev.this_device = NULL;
    return -EBADF;
  }
  spin_lock_init(&open_lock);
  spin_lock_init(&release_lock);
  // Initialize the hashtable.
  hash_init(tbl);

  return 0;
}

static void __exit uaf_exit(void) {
  /* Unregister virtual device */
  if (step_dev.this_device) misc_deregister(&step_dev);

  log("kernel module unloaded");
}

module_init(uaf_init);
module_exit(uaf_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("UAF S.H.I.E.L.D");
MODULE_DESCRIPTION("UAF SHIELD Protection");
