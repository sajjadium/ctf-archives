// Copyright (C) 2022? 2023? hxp. License expires after HXP CTF 2022
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

#include "hypersecure-mm.h"
#include "hypersecure-debug.h"
#include "hypersecure.h"

#include <asm/pgtable.h>
#include <linux/kernel.h>
#include <linux/gfp.h>
#include <linux/slab.h>
#include <linux/types.h>
#include <asm/io.h>
#include <linux/vmalloc.h>
#include <linux/mm.h>
#include <asm/set_memory.h>
#include <asm/tlbflush.h>

int hypersecure_mm_write_phys_memory(struct hypersecure_mm *mm, u64 phys_address, const void *bytes, u64 num_bytes) {
	if (phys_address + num_bytes > hypersecure_MAX_PHYS_SIZE) {
		return -EINVAL;
	}
	memcpy((unsigned char *)mm->phys_map + phys_address, bytes, num_bytes);
	return 0;
}

static void hypersecure_destroy_nested_table(struct hypersecure_mm *mm);

static int hypersecure_construct_nested_table(struct hypersecure_mm *mm) {
	int r;
	size_t page_i;
	const size_t num_pages = 4;
	struct hypersecure_nested_table_pml4 *pml4 = &mm->pml4;
	struct hypersecure_nested_table_pt* pt;

	// So, here we want to create the NPT with only four 4KiB pages.
	mm->phys_memory_pages = (struct page **)vmalloc(num_pages * sizeof(struct page *));
	if (!mm->phys_memory_pages) {
		r = -ENOMEM;
		goto fail;
	}
	memset(mm->phys_memory_pages, 0, num_pages * sizeof(struct page *));

	for (page_i = 0; page_i < num_pages; ++page_i) {
		mm->phys_memory_pages[page_i] = alloc_page(GFP_KERNEL);
		if (!mm->phys_memory_pages[page_i]) {
			r = -ENOMEM;
			goto fail;
		}
	}

	mm->phys_map = vmap(mm->phys_memory_pages, num_pages, VM_MAP, PAGE_KERNEL);
	if (!mm->phys_map) {
		r = -ENOMEM;
		goto fail;
	}
	memset(mm->phys_map, 0, hypersecure_MAX_PHYS_SIZE);

	// Create root.
	pml4->va = (void *)get_zeroed_page(GFP_KERNEL);
	if (!pml4->va) {
		r = -ENOMEM;
		goto fail;
	}
	pml4->pa = virt_to_phys(pml4->va);

	// Create pdp
	pml4->pdp.va = (void *)get_zeroed_page(GFP_KERNEL);
	if (!pml4->pdp.va) {
		r = -ENOMEM;
		goto fail;
	}
	pml4->pdp.pa = virt_to_phys(pml4->pdp.va);
	pml4->va[0] = hypersecure_create_entry(pml4->pdp.pa, hypersecure_PRESENT_MASK | hypersecure_WRITEABLE_MASK | hypersecure_USER_MASK);

	// Create pd
	pml4->pdp.pd.va = (void *)get_zeroed_page(GFP_KERNEL);
	if (!pml4->pdp.pd.va) {
		r = -ENOMEM;
		goto fail;
	}
	pml4->pdp.pd.pa = virt_to_phys(pml4->pdp.pd.va);
	pml4->pdp.va[0] = hypersecure_create_entry(pml4->pdp.pd.pa, hypersecure_PRESENT_MASK | hypersecure_WRITEABLE_MASK | hypersecure_USER_MASK);

	pt = &pml4->pdp.pd.pde[0];
	pt->va = (void *)get_zeroed_page(GFP_KERNEL);
	if (!pt->va) {
		r = -ENOMEM;
		goto fail;
	}
	pt->pa = virt_to_phys(pt->va);
	pml4->pdp.pd.va[0] = hypersecure_create_entry(pt->pa, hypersecure_PRESENT_MASK | hypersecure_WRITEABLE_MASK | hypersecure_USER_MASK);

	// Here are the PTEs. It's only four PTEs (16KiB).
	for (page_i = 0; page_i < num_pages; ++page_i) {
		u64 pte_pa = page_to_phys(mm->phys_memory_pages[page_i]);
		pt->va[page_i] = hypersecure_create_entry(pte_pa, hypersecure_PRESENT_MASK | hypersecure_WRITEABLE_MASK | hypersecure_USER_MASK);
	}

	mm->num_pages = num_pages;

	return 0;

fail:
	hypersecure_destroy_nested_table(mm);
	return r;
}

static void hypersecure_destroy_nested_table(struct hypersecure_mm *mm) {
	size_t i;
	struct hypersecure_nested_table_pml4 *pml4 = &mm->pml4;

	// Free memory for the page table and unmap.
	if (pml4->va) {
		free_page((unsigned long)pml4->va);
	}
	if (pml4->pdp.va) {
		free_page((unsigned long)pml4->pdp.va);
	}
	if (pml4->pdp.pd.va) {
		free_page((unsigned long)pml4->pdp.pd.va);
	}
	if (pml4->pdp.pd.pde[0].va) {
		free_page((unsigned long)pml4->pdp.pd.pde[0].va);
	}
	if (mm->phys_map) {
		vunmap(mm->phys_map);
	}

	// Free the physmem
	for (i = 0; i < mm->num_pages; ++i) {
		if (mm->phys_memory_pages[i]) {
		__free_page(mm->phys_memory_pages[i]);
		}
	}
	mm->phys_memory_pages = NULL;
}

static int hypersecure_construct_gpt(struct hypersecure_mm *mm) {
	const __u64 pml4e = hypersecure_create_entry(0x1000, hypersecure_PRESENT_MASK | hypersecure_WRITEABLE_MASK);
	const __u64 pdpe = hypersecure_create_entry(0x2000, hypersecure_PRESENT_MASK | hypersecure_WRITEABLE_MASK);
	const __u64 pde = hypersecure_create_entry(0x0000, hypersecure_PRESENT_MASK | hypersecure_WRITEABLE_MASK | hypersecure_LEAF_MASK);
	int r = 0;

	// The GPT will map the first 2MiB of GPA to avoid those few more lines...
	if ((r = hypersecure_mm_write_phys_memory(mm, 0x0, (void *)&pml4e, sizeof(pml4e))) != 0) {
		return r;
	}
	if ((r = hypersecure_mm_write_phys_memory(mm, 0x1000, (void *)&pdpe, sizeof(pdpe))) != 0) {
		return r;
	}
	if ((r = hypersecure_mm_write_phys_memory(mm, 0x2000, (void *)&pde, sizeof(pde))) != 0) {
		return r;
	}
	return 0;
}

static void hypersecure_mm_tlb_flush_on_cpu(void *info) {
	asm volatile(
		"mov %%cr4, %%rax\n\t"
		"mov %%rax, %%rbx\n\t"
		"xor $0x80, %%rbx\n\t" // Clear PGE
		"mov %%rbx, %%cr4\n\t" // Update CR4
		"mov %%rax, %%cr4\n\t" // Restore CR4
		: : : "%rax", "%rbx", "memory");
}

int hypersecure_create_mm(struct hypersecure_mm **out_mm) {
	struct hypersecure_mm *mm = NULL;
	int r;

	mm = kzalloc(sizeof(*mm), GFP_KERNEL);
	if (!mm) {
		r = -ENOMEM;
		goto fail;
	}

	// NPT
	r = hypersecure_construct_nested_table(mm);
	if (r) {
		hypersecure_log_msg("Failed to create NPT\n");
		kfree(mm);
		goto fail;
	}

	// GPT
	r = hypersecure_construct_gpt(mm);
	if (r) {
		hypersecure_log_msg("Failed to create GPT\n");
		hypersecure_destroy_nested_table(mm);
		kfree(mm);
		goto fail;
	}

	*out_mm = mm;

	return 0;

fail:
	return r;
}

void hypersecure_destroy_mm(struct hypersecure_mm *mm) {
	BUG_ON(!mm);

	on_each_cpu(hypersecure_mm_tlb_flush_on_cpu, NULL, 1);

	hypersecure_destroy_nested_table(mm);

	kfree(mm);
}

