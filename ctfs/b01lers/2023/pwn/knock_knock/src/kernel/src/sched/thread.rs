use core::sync::atomic::AtomicUsize;

use crate::linked_list::{ListNode, ListNodeData};
use crate::mem::MemOwner;
use super::kernel_stack::KernelStack;
use crate::prelude::*;

#[derive(Debug, Clone, Copy)]
pub enum ThreadState {
    Running,
    Ready,
    Dead,
}

#[derive(Debug)]
pub struct Thread {
    pub state: ThreadState,
    pub rsp: AtomicUsize,
    kernel_stack: KernelStack,

    list_node_data: ListNodeData<Thread>,
}

impl Thread {
    pub fn new(kernel_stack: KernelStack, rsp: usize) -> MemOwner<Thread> {
        MemOwner::new(
            Thread {
                state: ThreadState::Ready,
                rsp: AtomicUsize::new(rsp),
                kernel_stack,
                list_node_data: ListNodeData::default(),
            },
        )
    }

    pub fn syscall_rsp(&self) -> usize {
        self.kernel_stack.stack_top().as_usize()
    }
}

impl ListNode for Thread {
    fn list_node_data(&self) -> &ListNodeData<Self> {
        &self.list_node_data
    }
}
