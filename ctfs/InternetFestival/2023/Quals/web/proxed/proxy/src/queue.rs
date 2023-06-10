use std::collections::VecDeque;
use std::sync::{Mutex, Condvar};

#[derive(Debug)]
pub struct BlockingQueue<T>{
    queue : Mutex<VecDeque<T>>,
    condvar : Condvar,
}

impl<T> BlockingQueue<T>{
    pub fn new() -> Self{
        Self {
            queue : Mutex::new(VecDeque::new()),
            condvar : Condvar::new(),
        }
    }

    pub fn push(&self, value : T){
        let mut queue = self.queue.lock().unwrap();
        queue.push_back(value);

        self.condvar.notify_one();
    }

    pub fn pop(&self) -> T{
        let mut queue = self.queue.lock().unwrap();

        while queue.is_empty(){
            queue = self.condvar.wait(queue).unwrap();
        }

        queue.pop_front().unwrap()
    }
}