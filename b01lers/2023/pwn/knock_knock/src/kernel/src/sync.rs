use core::ops::{Deref, DerefMut};

use spin::{Mutex, MutexGuard};

use crate::arch::x64::IntDisable;

#[derive(Debug)]
pub struct IMutex<T: ?Sized>(Mutex<T>);

impl<T> IMutex<T> {
    pub const fn new(user_data: T) -> Self {
        IMutex(Mutex::new(user_data))
    }

    pub fn into_inner(self) -> T {
        self.0.into_inner()
    }

    pub fn lock(&self) -> IMutexGuard<T> {
        let int_disable = IntDisable::new();
        IMutexGuard(self.0.lock(), int_disable)
    }

    pub fn try_lock(&self) -> Option<IMutexGuard<T>> {
        let int_disable = IntDisable::new();
        self.0.try_lock().map(|guard| IMutexGuard(guard, int_disable))
    }

    pub unsafe fn force_unlock(&self) {
        unsafe {
            self.0.force_unlock();
        }
    }
}

impl<T: ?Sized + Default> Default for IMutex<T> {
    fn default() -> IMutex<T> {
        IMutex::new(Default::default())
    }
}

unsafe impl<T: ?Sized + Send> Send for IMutex<T> {}
unsafe impl<T: ?Sized + Send> Sync for IMutex<T> {}

#[derive(Debug)]
pub struct IMutexGuard<'a, T: ?Sized + 'a>(MutexGuard<'a, T>, IntDisable);

impl<T> Deref for IMutexGuard<'_, T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<T> DerefMut for IMutexGuard<'_, T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}
