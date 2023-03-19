use core::sync::atomic::{AtomicUsize, Ordering};

use crate::prelude::*;
use crate::arch::x64::{gs_addr, wrmsr, GSBASEK_MSR, GSBASE_MSR};

#[repr(C)]
#[derive(Debug)]
pub struct GsData {
    pub self_addr: AtomicUsize,
    pub syscall_rsp: AtomicUsize,
}

impl GsData {
    pub fn set_self_addr(&self) {
        self.self_addr.store((self as *const _) as _, Ordering::Release);
    }
}

pub fn init() {
    let gs_data = GsData {
        self_addr: AtomicUsize::new(0),
        syscall_rsp: AtomicUsize::new(0),
    };

    let gs_data = Box::new(gs_data);
    gs_data.set_self_addr();

    let ptr = Box::into_raw(gs_data) as *mut _;
    
    wrmsr(GSBASE_MSR, ptr as u64);
    wrmsr(GSBASEK_MSR, ptr as u64);
}

pub fn cpu_local_data() -> &'static GsData {
    unsafe { (gs_addr() as *const GsData).as_ref().unwrap() }
}