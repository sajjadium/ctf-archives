use core::ops::{Deref, DerefMut};

use crate::prelude::*;

#[derive(Debug)]
pub struct MemOwner<T>(*mut T);

impl<T> MemOwner<T> {
    pub fn new(data: T) -> Self {
        Self(Box::leak(Box::new(data)))
    }

    pub unsafe fn new_at_addr(data: T, addr: usize) -> Self {
        let ptr = addr as *mut T;
        unsafe {
            ptr.write(data);
        }
        MemOwner(ptr)
    }

    pub unsafe fn from_raw(ptr: *mut T) -> Self {
        MemOwner(ptr)
    }

    pub unsafe fn clone(&self) -> Self {
        MemOwner(self.0)
    }

    pub fn ptr(&self) -> *const T {
        self.0 as *const T
    }

    pub fn ptr_mut(&self) -> *mut T {
        self.0
    }

    pub fn leak<'a>(mut self) -> &'a mut T
        where Self: 'a {
        unsafe { unbound_mut(&mut *self) }
    }

    pub unsafe fn drop_in_place(self) {
        unsafe {
            drop(Box::from_raw(self.0));
        }
    }
}

impl<T> Deref for MemOwner<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        unsafe { self.0.as_ref().unwrap() }
    }
}

impl<T> DerefMut for MemOwner<T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        unsafe { self.0.as_mut().unwrap() }
    }
}

unsafe impl<T: Send> Send for MemOwner<T> {}
unsafe impl<T: Sync> Sync for MemOwner<T> {}
