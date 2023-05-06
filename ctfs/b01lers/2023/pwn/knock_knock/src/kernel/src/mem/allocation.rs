use core::alloc::Layout;
use core::cmp::min;

use super::VirtAddr;
use crate::prelude::*;

#[derive(Debug, Clone, Copy)]
pub struct Allocation {
    ptr: VirtAddr,
    size: usize,
}

impl Allocation {
    pub fn new(addr: usize, size: usize) -> Self {
        Allocation {
            ptr: VirtAddr::new(addr),
            size,
        }
    }

    pub fn addr(&self) -> VirtAddr {
        self.ptr
    }

    pub fn phys_addr(&self) -> PhysAddr {
        self.ptr.to_phys()
    }

    pub fn as_ptr<T>(&self) -> *const T {
        self.ptr.as_ptr()
    }

    pub fn as_mut_ptr<T>(&mut self) -> *mut T {
        self.ptr.as_mut_ptr()
    }

    pub fn as_slice(&self) -> &[u8] {
        unsafe { core::slice::from_raw_parts(self.as_ptr(), self.size) }
    }

    pub fn as_mut_slice(&mut self) -> &mut [u8] {
        unsafe { core::slice::from_raw_parts_mut(self.as_mut_ptr(), self.size) }
    }

    pub fn as_vrange(&self) -> UVirtRange {
        UVirtRange::new(self.ptr, self.size)
    }

    pub fn as_usize(&self) -> usize {
        self.ptr.as_usize()
    }

    pub fn size(&self) -> usize {
        self.size
    }

    pub fn copy_from_mem(&mut self, other: &[u8]) -> usize {
        let size = min(self.size(), other.len());
        unsafe {
            let dst: &mut [u8] = core::slice::from_raw_parts_mut(self.as_mut_ptr(), size);
            let src: &[u8] = core::slice::from_raw_parts(other.as_ptr(), size);
            dst.copy_from_slice(src);
        }
        size
    }
}

#[derive(Debug, Clone, Copy)]
pub struct HeapAllocation {
    addr: usize,
    size: usize,
    align: usize,
}

impl HeapAllocation {
    pub fn new(addr: usize, size: usize, align: usize) -> Self {
        HeapAllocation {
            addr,
            size,
            align,
        }
    }

    pub fn from_layout(addr: usize, layout: Layout) -> Self {
        Self::new(addr, layout.size(), layout.align())
    }

    pub fn from_ptr<T>(ptr: *const T) -> Self {
        Self::from_layout(ptr as usize, Layout::new::<T>())
    }

    pub fn array<T>(ptr: *const T, len: usize) -> Self {
        Self::from_layout(ptr as usize, Layout::array::<T>(len).expect("Layout overflowed"))
    }

    pub fn addr(&self) -> usize {
        self.addr
    }

    pub fn end_addr(&self) -> usize {
        self.addr + self.size
    }

    pub fn size(&self) -> usize {
        self.size
    }

    pub fn align(&self) -> usize {
        self.align
    }

    pub fn as_ptr<T>(&self) -> *const T {
        self.addr as *const T
    }

    pub fn as_mut_ptr<T>(&mut self) -> *mut T {
        self.addr as *mut T
    }

    pub fn as_slice(&self) -> &[u8] {
        unsafe { core::slice::from_raw_parts(self.as_ptr(), self.size) }
    }

    pub fn as_mut_slice(&mut self) -> &mut [u8] {
        unsafe { core::slice::from_raw_parts_mut(self.as_mut_ptr(), self.size) }
    }

    pub fn copy_from_mem(&mut self, other: &[u8]) -> usize {
        let size = min(self.size(), other.len());
        unsafe {
            let dst: &mut [u8] = core::slice::from_raw_parts_mut(self.as_mut_ptr(), size);
            let src: &[u8] = core::slice::from_raw_parts(other.as_ptr(), size);
            dst.copy_from_slice(src);
        }
        size
    }
}
