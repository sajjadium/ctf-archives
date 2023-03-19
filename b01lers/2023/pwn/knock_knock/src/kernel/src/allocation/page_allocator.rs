use core::cell::Cell;

use crate::prelude::*;
use crate::linked_list::{LinkedList, ListNode, ListNodeData};
use crate::mb2::{MemoryMap, MemoryRegionType};
use crate::mem::{Allocation, MemOwner};
use crate::sync::IMutex;

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
}

impl ListNode for Node {
    fn list_node_data(&self) -> &ListNodeData<Self> {
        &self.list_node_data
    }
}

struct PageAllocatorInner {
    list: LinkedList<Node>,
    free_space: usize,
}

impl PageAllocatorInner {
    fn new(virt_range: AVirtRange) -> Self {
        let node = unsafe {
            Node::new(virt_range.as_usize(), virt_range.size())
        };

        let mut list = LinkedList::new();
        list.push(node);

        PageAllocatorInner {
            list,
            free_space: virt_range.size(),
        }
    }

    fn alloc(&mut self, size: usize) -> Option<Allocation> {
        assert!(page_aligned(size));

        if size > self.free_space {
            return None;
        }

        let mut out = None;

        let mut node = None;

        for free_zone in self.list.iter() {
            if free_zone.size() >= size {
                out = Some(Allocation::new(free_zone as *const _ as usize, size));
                node = Some(free_zone as *const _ as *mut Node);
                self.free_space -= size;
                break;
            }
        }

        if let Some(node) = node {
            let node_size = unsafe { (*node).size() };

            if node_size == size {
                unsafe {
                    self.list.remove_node(node);
                }
            } else {
                let new_node = unsafe {
                    Node::new(node as usize + size, node_size - size)
                };

                self.list.replace_node(node, new_node);
            }
        }

        out
    }

    unsafe fn dealloc(&mut self, allocation: Allocation) {
        let addr = allocation.as_usize();
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

        self.free_space += size;
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

pub struct PageAllocator {
    inner: IMutex<PageAllocatorInner>,
}

impl PageAllocator {
    pub unsafe fn new(memory_map: &MemoryMap) -> Self {
        let largest_zone = memory_map
            .iter()
            .filter(|zone| matches!(zone, MemoryRegionType::Usable(_)))
            .filter_map(|mem| mem.range().to_virt().as_inside_aligned())
            .reduce(|z1, z2| if z1.size() > z2.size() { z1 } else { z2 })
            .expect("no usable memory zones found");

        PageAllocator {
            inner: IMutex::new(PageAllocatorInner::new(largest_zone)),
        }
    }

    pub fn alloc(&self, size: usize) -> Option<Allocation> {
        self.inner.lock().alloc(size)
    }

    pub unsafe fn dealloc(&self, allocation: Allocation) {
        unsafe {
            self.inner.lock().dealloc(allocation);
        }
    }
}