use std::{
    ptr::NonNull,
    sync::atomic::{AtomicI32, AtomicU32, Ordering},
    ops::{Deref, DerefMut},
};

struct ObjBox<T: ?Sized> {
    strong_refs: AtomicU32,
    rw: AtomicI32,
    val: T,
}

impl<T> ObjBox<T> {
    fn new(val: T) -> Self {
        Self {
            strong_refs: AtomicU32::new(1),
            rw: AtomicI32::new(0),
            val
        }
    }
}

pub struct Ref<'b, T: ?Sized> {
    refobj: NonNull<T>,
    rw: &'b AtomicI32,
}

impl<'b, T: ?Sized> Deref for Ref<'b, T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        unsafe { self.refobj.as_ref() }
    }
}

impl<'b, T: ?Sized> Drop for Ref<'b, T> {
    fn drop(&mut self) {
        self.rw.fetch_sub(1, Ordering::Relaxed);
    }
}

pub struct RefMut<'b, T: ?Sized> {
    refobj: NonNull<T>,
    rw: &'b AtomicI32,
}

impl<'b, T: ?Sized + 'b> Deref for RefMut<'b, T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        unsafe { self.refobj.as_ref() }
    }
}

impl<'b, T: ?Sized + 'b> DerefMut for RefMut<'b, T> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        unsafe { self.refobj.as_mut() }
    }
}

impl<'b, T: ?Sized> Drop for RefMut<'b, T> {
    fn drop(&mut self) {
        self.rw.fetch_add(1, Ordering::Relaxed);
    }
}

#[derive(Debug)]
pub struct BorrowError;

#[derive(Debug)]
pub struct Obj<T: ?Sized> {
    inner: NonNull<ObjBox<T>>,
}

#[macro_export]
macro_rules! obj_new {
    ($val: expr, $dflt: expr $(,)?) => {
        {
            let val = $crate::obj::Obj::new($dflt);
            *val.borrow_mut() = $val;
            val
        }
    }
}

impl<T> Obj<T> {
    pub fn new(val: T) -> Self {
        Self {
            inner: Box::leak(Box::new(ObjBox::new(val))).into(),
        }
    }

    pub fn try_borrow<'b, 's: 'b>(&'s self) -> Result<Ref<'b, T>, BorrowError> {
        let inner = unsafe { self.inner.as_ref() };
        let mut ctr = inner.rw.load(Ordering::Relaxed);
        loop {
            if ctr < 0 {
                return Err(BorrowError);
            }

            match inner.rw.compare_exchange_weak(ctr, ctr + 1, Ordering::SeqCst, Ordering::Relaxed) {
                Ok(_) => break,
                Err(new_ctr) => ctr = new_ctr,
            }
        }

        return Ok(Ref {
            refobj: NonNull::from(&inner.val),
            rw: &inner.rw,
        })
    }

    pub fn try_borrow_mut<'b, 's: 'b>(&'s self) -> Result<RefMut<'b, T>, BorrowError> {
        let inner = unsafe { self.inner.as_ref() };
        let mut ctr = inner.rw.load(Ordering::Relaxed);
        loop {
            if ctr != 0 {
                return Err(BorrowError);
            }

            match inner.rw.compare_exchange_weak(ctr, -1, Ordering::SeqCst, Ordering::Relaxed) {
                Ok(_) => break,
                Err(new_ctr) => ctr = new_ctr,
            }
        }

        return Ok(RefMut {
            refobj: NonNull::from(&inner.val),
            rw: &inner.rw,
        })
    }

    pub fn borrow(&self) -> Ref<'_, T> {
        self.try_borrow().unwrap()
    }

    pub fn borrow_mut(&self) -> RefMut<'_, T> {
        self.try_borrow_mut().unwrap()
    }
}

impl<T: ?Sized> Obj<T> {
    unsafe fn gets(&self) {
        self.inner.as_ref().strong_refs.fetch_add(1, Ordering::Relaxed);
    }

    unsafe fn puts(&mut self) {
        let before = {
            let inner = self.inner.as_ref();
            inner.strong_refs.fetch_sub(1, Ordering::Relaxed)
        };

        if before <= 1 {
            drop(Box::from_raw(self.inner.as_ptr()));
        }
    }
}

impl<T: ?Sized> Drop for Obj<T> {
    fn drop(&mut self) {
        unsafe { self.puts() }
    }
}

impl<T: ?Sized> Clone for Obj<T> {
    fn clone(&self) -> Self {
        unsafe { self.gets() }
        Self { 
            inner: self.inner.clone(),
        }
    }
}

unsafe impl<T: ?Sized + Sync + Send> Sync for Obj<T> {}
unsafe impl<T: ?Sized + Sync + Send> Send for Obj<T> {}
