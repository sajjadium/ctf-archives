use crate::prelude::*;
use crate::mem::Allocation;
use crate::allocation::zm;

#[derive(Debug)]
pub enum KernelStack {
    Owned(Allocation),
    Existing(AVirtRange),
}

impl KernelStack {
    pub const DEFAULT_SIZE: usize = PAGE_SIZE * 16;

    pub fn new() -> KResult<Self> {
        let allocation = zm()
            .alloc(Self::DEFAULT_SIZE)
            .ok_or(SysErr::OutOfMem)?;
        
        Ok(KernelStack::Owned(allocation))
    }

    pub fn as_virt_range(&self) -> AVirtRange {
        match self {
            Self::Owned(allocation) => allocation.as_vrange().as_inside_aligned().unwrap(),
            Self::Existing(virt_range) => *virt_range,
        }
    }

    pub fn stack_base(&self) -> VirtAddr {
        self.as_virt_range().addr()
    }

    pub fn stack_top(&self) -> VirtAddr {
        self.as_virt_range().end_addr()
    }
}

impl Drop for KernelStack {
    fn drop(&mut self) {
        if let Self::Owned(allocation) = self {
            unsafe { zm().dealloc(*allocation); }
        }
    }
}