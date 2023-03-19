use spin::Once;

use crate::prelude::*;
use crate::mem::Allocation;
use crate::mb2::MemoryMap;
use crate::vmem_manager::{PageMappingFlags, ADDR_SPACE};
use crate::sync::IMutex;
use heap_allocator::LinkedListAllocator;
pub use page_allocator::PageAllocator;

mod heap_allocator;
mod page_allocator;


static PAGE_ALLOCATOR: Once<PageAllocator> = Once::new();

pub fn zm() -> &'static PageAllocator {
    PAGE_ALLOCATOR
        .get()
        .expect("zone manager (PageAllocator) has not been initilized")
}

#[global_allocator]
static HEAP: LinkedListAllocator = LinkedListAllocator::new();

pub unsafe fn init(mem_map: &MemoryMap) -> KResult<()> {
    PAGE_ALLOCATOR.call_once(|| unsafe { PageAllocator::new(mem_map) });

    Ok(())
}

static ALLOCATED_RANGES: IMutex<Vec<AVirtRange>> = IMutex::new(Vec::new());

pub fn alloc_at(virt_range: AVirtRange, flags: PageMappingFlags) -> KResult<()> {
    let allocation = zm()
        .alloc(virt_range.size())
        .ok_or(SysErr::OutOfMem)?;

    let mut addr_space = ADDR_SPACE.lock();

    if let Err(error) = addr_space.map_memory(virt_range, allocation.phys_addr(), flags) {
        unsafe { zm().dealloc(allocation); }

        Err(error)
    } else {
        let mut ranges = ALLOCATED_RANGES.lock();
        let index = ranges.binary_search_by_key(&virt_range.addr(), AVirtRange::addr)
            .expect_err("inconsistancy between ALLOCATED_RANGES and ADDR_SPACE");

        ranges.insert(index, virt_range);

        Ok(())
    }
}

pub fn dealloc_at(address: VirtAddr) -> KResult<()> {
    let mut addr_space = ADDR_SPACE.lock();
    let mut ranges = ALLOCATED_RANGES.lock();

    let range_index = ranges.binary_search_by_key(&address, AVirtRange::addr)
        .or(Err(SysErr::InvlVirtAddr))?;

    let range = ranges.remove(range_index);

    let address = addr_space.unmap_memory(range)?;

    let allocation = Allocation::new(address.to_virt().as_usize(), range.size());

    unsafe {
        zm().dealloc(allocation);
    }

    Ok(())
}