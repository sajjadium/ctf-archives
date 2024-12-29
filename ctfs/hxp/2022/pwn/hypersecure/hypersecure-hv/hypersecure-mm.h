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

#ifndef hypersecure_MM_H
#define hypersecure_MM_H

#include <linux/types.h>

#define hypersecure_MAX_PHYS_SIZE (4 * 4096)

struct hypersecure_nested_table_pt {
	u64 *va;
	u64 pa;
};

struct hypersecure_nested_table_pd {
	u64 *va;
	u64 pa;
	struct hypersecure_nested_table_pt pde[512];
};

struct hypersecure_nested_table_pdp {
	u64 *va;
	u64 pa;
	struct hypersecure_nested_table_pd pd;
};

struct hypersecure_nested_table_pml4 {
	u64 *va;
	u64 pa;
	struct hypersecure_nested_table_pdp pdp;
};

struct hypersecure_mm {
	struct hypersecure_nested_table_pml4 pml4;
	struct page **phys_memory_pages;
	size_t num_pages;
	void *phys_map;
};

int hypersecure_create_mm(struct hypersecure_mm **mm);
void hypersecure_destroy_mm(struct hypersecure_mm *mm);

int hypersecure_mm_write_phys_memory(struct hypersecure_mm *mm, u64 phys_address, const void *bytes, u64 num_bytes);
int hypersecure_mm_write_virt_memory(struct hypersecure_mm *mm, u64 virt_address, void *bytes, u64 num_bytes);

int hypersecure_allocate_phys_page(struct hypersecure_mm *mm, u64 phys_address);

#endif // hypersecure_MM_H
