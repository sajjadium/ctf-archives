use crate::linked_list::LinkedList;
use super::thread::Thread;
use crate::mem::MemOwner;
use crate::sync::IMutex;
use crate::prelude::*;

#[derive(Debug)]
pub struct ThreadMap {
    ready_threads: IMutex<LinkedList<Thread>>,
}

impl ThreadMap {
    pub const fn new() -> Self {
        ThreadMap {
            ready_threads: IMutex::new(LinkedList::new()),
        }
    }

    pub fn get_ready_thread(&self) -> Option<MemOwner<Thread>> {
        self.ready_threads.lock().pop_front()
    }

    pub fn insert_ready_thread(&self, thread_handle: MemOwner<Thread>) {
        self.ready_threads.lock().push(thread_handle);
    }
}

unsafe impl Send for ThreadMap {}
unsafe impl Sync for ThreadMap {}