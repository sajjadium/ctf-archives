#include "../includes/memory.h"
#include <linux/slab.h>
#include <linux/mm.h>
#include <linux/list.h>
#include <asm/io.h>
#include <linux/gfp.h>

#define MAX_VM_SIZE 0x200000

__u64 get_ept_entry(__u64 paddr, int level) {
    switch (level) {
        case 0:
            {
                EPT_PTE ept;
                ept.fields.read = 1;
                ept.fields.write = 1;
                ept.fields.execute = 1;
                ept.fields.eptMemoryType = 6;
                ept.fields.ignorePAT = 1;
                ept.fields.accessedFlag = 1;
                ept.fields.dirtyFlag = 1;
                ept.fields.executeForUserMode = 1;
                ept.fields.physicalAddress = paddr / 0x1000;
                return ept.all;
            }
        case 1:
        case 2:
        case 3:
            {
                EPT_PDE ept;
                ept.all = 0;
                ept.fields.read = 1;
                ept.fields.write = 1;
                ept.fields.execute = 1;
                ept.fields.executeForUserMode = 0;
                ept.fields.physicalAddress = paddr / PAGE_SIZE;
                return ept.all;
            }
        case 4:
            {
                EPTP ept;
                ept.all = 0;
                ept.fields.memoryType = 6;
                ept.fields.pageWalkLength = 4 - 1;
                ept.fields.dirtyAndAceessEnabled = 1;
                ept.fields.reserved1 = 0;
                ept.fields.PML4Address = paddr / PAGE_SIZE;
                ept.fields.reserved2 = 0;
                return ept.all;
            }
        default:
            return 0;
    }
}

mapping_t *find_mapping(memory_t *mem, __u64 paddr) {
    mapping_t *mapping;
    paddr &= ~0xfff;
    hash_for_each_possible(mem->maps, mapping, map, paddr) {
        if (mapping->paddr == paddr)
            return mapping;
    }
    return NULL;
}

mapping_t *get_new_ept_page(memory_t *mem, __u64 paddr, int level) {
    mapping_t *map = find_mapping(mem, paddr);
    if (map && level == 0) {
        return map;
    } 
    map = kmalloc(sizeof(mapping_t), GFP_KERNEL);
    if (!map)
        return NULL;
    if (!level)
        map->paddr = paddr;
    else
        map->paddr = (__u64)-1LL;
    map->page = alloc_page(GFP_KERNEL);
    memset(page_to_virt(map->page), 0, 0x1000);
    hash_add(mem->maps, &map->map, map->paddr);
    return map;
}

mapping_t *get_new_mmap_page(memory_t *mem, __u64 paddr) {
    mapping_t *map;
    map = find_mapping(mem, paddr);
    if (map)
        return map;
    else {
        map = kmalloc(sizeof(mapping_t), GFP_KERNEL);
        if (!map)
            return NULL;
        map->page = alloc_page(GFP_KERNEL);
        memset(page_to_virt(map->page), 0, 0x1000);
        map->paddr = paddr;
        hash_add(mem->maps, &map->map, map->paddr);
    }
    return map;
}

mapping_t *_handle_ept_violation(memory_t *mem, __u64 paddr, int level, __u64 curr) {
    __u64 index = (paddr >> ((level * 9) + 12) ) & 0x1ff;
    __u64 phys = curr & ~0xfff;
    __u64 *ptr = (__u64 *)phys_to_virt(phys);
    mapping_t *map;

    if (!ptr[index]) {
        map = get_new_ept_page(mem, paddr, level);
        if (!map)
            return NULL;
        curr = get_ept_entry(page_to_phys(map->page), level);
        ptr[index] = curr;
        if (level == 0)
            return map;
    } else {
        if (level == 0)
            return NULL;
        curr = ptr[index];
    }

    return _handle_ept_violation(mem, paddr,level - 1, curr);
}

mapping_t *handle_mmap_fault(memory_t *mem, __u64 paddr) {
    return get_new_mmap_page(mem, paddr);
}

mapping_t *handle_ept_violation(memory_t *mem, __u64 paddr, __u64 eptp){
    return _handle_ept_violation(mem, paddr, 3, eptp);
}

void destroy_mem(memory_t *mem) {
    struct hlist_node *tmp;
    mapping_t *e;
    int i;

    hash_for_each_safe(mem->maps, i, tmp, e, map) {
        __free_page(e->page);    
        kfree(e);
    }
    kfree(mem);
}

memory_t *alloc_mem(void) {
    memory_t *mem = kmalloc(sizeof(memory_t), GFP_KERNEL);
    mapping_t * ept_map;
    struct page * plm4_page;
    if (!mem) {
        return NULL;
    }

    ept_map = kmalloc(sizeof(mapping_t), GFP_KERNEL);
    if (!ept_map) {
        return NULL;
    }

    plm4_page = alloc_page(GFP_KERNEL);
    memset(page_to_virt(plm4_page), 0, 0x1000);
    ept_map->page = plm4_page;
    ept_map->paddr = (__u64)-1LL;

    hash_init(mem->maps);
    hash_add(mem->maps, &ept_map->map, ept_map->paddr);

    mem->eptp[0] = get_ept_entry(page_to_phys(plm4_page), 4);

    return mem;
}
