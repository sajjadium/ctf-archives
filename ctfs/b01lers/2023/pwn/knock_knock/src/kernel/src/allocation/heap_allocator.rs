use core::cell::Cell;
use core::cmp::max;
use core::mem;
use alloc::alloc::GlobalAlloc;

use super::zm;
use crate::linked_list::{LinkedList, ListNode, ListNodeData};
use crate::mem::{Allocation, HeapAllocation, Layout, MemOwner};
use crate::prelude::*;
use crate::sync::IMutex;

const HEAP_ZONE_SIZE: usize = PAGE_SIZE * 8;
const CHUNK_SIZE: usize = 1 << log2_up_const(mem::size_of::<Node>());
const INITIAL_CHUNK_SIZE: usize = align_up(mem::size_of::<HeapZone>(), CHUNK_SIZE);

#[derive(Debug, Clone, Copy)]
enum ResizeResult {
    Shrink(usize),
    Remove(usize),
    NoCapacity,
}

#[derive(Debug)]
struct Node {
    list_node_data: ListNodeData<Self>,
    size: Cell<usize>,
}

impl Node {
    unsafe fn new(addr: usize, size: usize) -> MemOwner<Self> {
        let out = Node {
            list_node_data: ListNodeData::default(),
            size: Cell::new(size),
        };

        unsafe { MemOwner::new_at_addr(out, addr) }
    }

    unsafe fn resize(&self, size: usize, align: usize) -> ResizeResult {
        let self_size = self.size();
        if size > self_size {
            return ResizeResult::NoCapacity;
        }

        let naddr = align_down(self.addr() + (self_size - size), max(align, CHUNK_SIZE));
        if naddr < self.addr() {
            return ResizeResult::NoCapacity;
        }

        let nsize = naddr - self.addr();
        if nsize >= CHUNK_SIZE {
            self.set_size(nsize);
            ResizeResult::Shrink(naddr)
        } else {
            ResizeResult::Remove(naddr)
        }
    }

    fn merge<'a>(&'a self, node: &'a Node) -> bool {
        if self.addr() + self.size() == node.addr() {
            self.size.set(self.size() + node.size());
            true
        } else {
            false
        }
    }

    fn size(&self) -> usize {
        self.size.get()
    }

    fn set_size(&self, size: usize) {
        self.size.set(size);
    }
}

impl ListNode for Node {
    fn list_node_data(&self) -> &ListNodeData<Self> {
        &self.list_node_data
    }
}

struct HeapZone {
    list_node_data: ListNodeData<Self>,
    mem: Allocation,
    free_space: Cell<usize>,
    list: LinkedList<Node>,
}

impl HeapZone {
    unsafe fn new(size: usize) -> Option<MemOwner<Self>> {
        let mem = zm().alloc(size)?;
        let size = mem.size();
        let ptr = mem.as_usize() as *mut HeapZone;

        let mut out = HeapZone {
            list_node_data: ListNodeData::default(),
            mem,
            free_space: Cell::new(size - INITIAL_CHUNK_SIZE),
            list: LinkedList::new(),
        };

        let node = unsafe { Node::new(mem.as_usize() + INITIAL_CHUNK_SIZE, size - INITIAL_CHUNK_SIZE) };
        out.list.push(node);

        unsafe {
            ptr.write(out);
            Some(MemOwner::from_raw(ptr))
        }
    }

    fn free_space(&self) -> usize {
        self.free_space.get()
    }

    fn contains(&self, addr: usize, size: usize) -> bool {
        (addr >= self.addr() + CHUNK_SIZE) && (addr + size <= self.addr() + CHUNK_SIZE + self.mem.size())
    }

    unsafe fn alloc(&mut self, layout: Layout) -> Option<HeapAllocation> {
        let size = layout.size();
        let align = layout.align();

        if size > self.free_space() {
            return None;
        }

        let mut out = None;
        let mut rnode = None;

        for free_zone in self.list.iter_mut() {
            let old_size = free_zone.size();
            if old_size >= size {
                match unsafe { free_zone.resize(size, align) } {
                    ResizeResult::Shrink(addr) => {
                        let alloc_size = old_size - free_zone.size();
                        let free_space = self.free_space();
                        self.free_space.set(free_space - alloc_size);
                        out = Some(HeapAllocation::new(addr, alloc_size, align));
                        break;
                    },
                    ResizeResult::Remove(addr) => {
                        rnode = Some(free_zone as *mut Node);
                        self.free_space.set(self.free_space() - old_size);
                        out = Some(HeapAllocation::new(addr, old_size, align));
                        break;
                    },
                    ResizeResult::NoCapacity => continue,
                }
            }
        }

        if let Some(node) = rnode {
            unsafe {
                self.list.remove_node(node);
            }
        }

        out
    }

    unsafe fn dealloc(&mut self, allocation: HeapAllocation) {
        let addr = allocation.addr();
        let size = allocation.size();

        let cnode = unsafe { Node::new(addr, size) };
        let (pnode, nnode) = self.get_prev_next_node(addr);

        let cnode = if let Some(pnode) = pnode {
            unsafe {
                if (*pnode).merge(&cnode) {
                    pnode
                } else {
                    self.list.insert_after(cnode, pnode)
                }
            }
        } else {
            self.list.push_front(cnode)
        };

        if let Some(nnode) = nnode {
            unsafe {
                if (*cnode).merge(&*nnode) {
                    self.list.remove_node(nnode);
                }
            }
        }

        self.free_space.set(self.free_space() + size);
    }

    fn get_prev_next_node(&self, addr: usize) -> (Option<*mut Node>, Option<*mut Node>) {
        let mut pnode = None;
        let mut nnode = None;
        for region in self.list.iter() {
            if region.addr() > addr {
                nnode = Some(region as *const _ as *mut _);
                break;
            }
            pnode = Some(region as *const _ as *mut _);
        }

        (pnode, nnode)
    }
}

impl ListNode for HeapZone {
    fn list_node_data(&self) -> &ListNodeData<Self> {
        &self.list_node_data
    }
}

struct LinkedListAllocatorInner {
    list: LinkedList<HeapZone>,
}

impl LinkedListAllocatorInner {
    const fn new() -> Self {
        LinkedListAllocatorInner {
            list: LinkedList::new(),
        }
    }

    fn alloc(&mut self, layout: Layout) -> Option<HeapAllocation> {
        let size = layout.size();
        let align = layout.align();

        for z in self.list.iter_mut() {
            if z.free_space() >= size {
                if let Some(allocation) = unsafe { z.alloc(layout) } {
                    return Some(allocation);
                }
            }
        }

        let size_inc = max(HEAP_ZONE_SIZE, size + max(align, CHUNK_SIZE) + INITIAL_CHUNK_SIZE);
        let zone = match unsafe { HeapZone::new(size_inc) } {
            Some(n) => n,
            None => return None,
        };

        let zone = self.list.push(zone);

        unsafe { zone.alloc(layout) }
    }

    unsafe fn dealloc(&mut self, allocation: HeapAllocation) {
        let addr = allocation.addr();
        let size = allocation.size();

        for z in self.list.iter_mut() {
            if z.contains(addr, size) {
                unsafe {
                    z.dealloc(allocation);
                }
                return;
            }
        }

        panic!("invalid allocation passed to dealloc");
    }

    fn compute_alloc_properties(allocation: HeapAllocation) -> Option<HeapAllocation> {
        if align_of(allocation.addr()) < CHUNK_SIZE {
            None
        } else {
            let align = allocation.align();
            let size = align_up(allocation.size(), max(CHUNK_SIZE, align));
            Some(HeapAllocation::new(allocation.addr(), size, align))
        }
    }
}

pub struct LinkedListAllocator {
    inner: IMutex<LinkedListAllocatorInner>,
}

impl LinkedListAllocator {
    pub const fn new() -> Self {
        LinkedListAllocator {
            inner: IMutex::new(LinkedListAllocatorInner::new()),
        }
    }
}

unsafe impl GlobalAlloc for LinkedListAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        let allocation = self.inner.lock().alloc(layout);

        match allocation {
            Some(mut allocation) => allocation.as_mut_ptr(),
            None => null_mut(),
        }
    }

    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        let allocation = HeapAllocation::from_layout(ptr as usize, layout);
        let allocation = LinkedListAllocatorInner::compute_alloc_properties(allocation)
            .expect("invalid layout passed to dealloc");

        unsafe { self.inner.lock().dealloc(allocation) }
    }
}
