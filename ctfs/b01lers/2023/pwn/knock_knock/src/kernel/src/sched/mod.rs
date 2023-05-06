pub mod kernel_stack;
mod thread;
mod thread_map;

use core::sync::atomic::{AtomicU64, AtomicPtr, Ordering};
use core::time::Duration;
use core::slice;

pub use thread::{ThreadState, Thread};
use thread_map::ThreadMap;
use crate::arch::x64::{IntDisable, asm_switch_thread, asm_thread_init};
use crate::mem::MemOwner;
use crate::prelude::*;
use crate::int::{self, pit};
use crate::gdt::TSS;
use crate::sync::IMutex;
use kernel_stack::KernelStack;

pub const SCHED_TIME: Duration = Duration::from_millis(10);

pub static THREAD_MAP: ThreadMap = ThreadMap::new();

pub static LAST_THREAD_SWITCH_NSEC: AtomicU64 = AtomicU64::new(0);

pub static CURRENT_THREAD_HANDLE: AtomicPtr<Thread> = AtomicPtr::new(null_mut());

pub static POST_SWITCH_DATA: IMutex<Option<PostSwitchData>> = IMutex::new(None);

pub fn timer_handler() {
    let current_nsec = pit().nsec_no_latch();
    let last_switch_nsec = LAST_THREAD_SWITCH_NSEC.load(Ordering::Acquire);

    if current_nsec - last_switch_nsec > SCHED_TIME.as_nanos() as u64 {
        let _ = switch_current_thread_to(
            ThreadState::Ready,
            IntDisable::new(),
            PostSwitchAction::SendEoi,
        );
    }
}

#[derive(Debug)]
pub struct PostSwitchData {
    old_thread_handle: MemOwner<Thread>,
    post_switch_action: PostSwitchAction,
}

#[derive(Debug)]
pub enum PostSwitchAction {
    None,
    SendEoi,
}

#[no_mangle]
extern "C" fn post_switch_handler(old_rsp: usize) {
    let mut post_switch_data = POST_SWITCH_DATA.lock();
    let PostSwitchData {
        old_thread_handle,
        post_switch_action,
    } = core::mem::replace(&mut *post_switch_data, None)
        .expect("post switch data was none after switching threads");

    old_thread_handle.rsp.store(old_rsp, Ordering::Release);

    match old_thread_handle.state {
        ThreadState::Running => unreachable!(),
        ThreadState::Ready => THREAD_MAP.insert_ready_thread(old_thread_handle),
        ThreadState::Dead => unsafe {
            old_thread_handle.drop_in_place();
        },
    }

    match post_switch_action {
        PostSwitchAction::None => (),
        PostSwitchAction::SendEoi => int::eoi(),
    }
}

#[derive(Debug)]
pub enum ThreadSwitchToError {
    NoAvailableThreads,
    InvalidState,
}

pub fn switch_current_thread_to(state: ThreadState, _int_disable: IntDisable, post_switch_hook: PostSwitchAction) -> Result<(), ThreadSwitchToError> {
    if matches!(state, ThreadState::Running) {
        return Err(ThreadSwitchToError::InvalidState);
    }

    let mut new_thread_handle = THREAD_MAP.get_ready_thread()
        .ok_or(ThreadSwitchToError::NoAvailableThreads)?;

    let new_thread = unsafe {
        new_thread_handle
            .ptr()
            .as_ref()
            .unwrap()
    };

    let old_thread_handle = CURRENT_THREAD_HANDLE.swap(new_thread_handle.ptr_mut(), Ordering::AcqRel);
    let mut old_thread_handle = unsafe { MemOwner::from_raw(old_thread_handle) };

    old_thread_handle.state = state;
    new_thread_handle.state = ThreadState::Running;

    let new_rsp = new_thread.rsp.load(Ordering::Acquire);

    cpu_local_data().syscall_rsp.store(new_thread.syscall_rsp(), Ordering::Release);
    TSS.lock().rsp0 = new_thread.syscall_rsp() as u64;

    *POST_SWITCH_DATA.lock() = Some(PostSwitchData {
        old_thread_handle,
        post_switch_action: post_switch_hook,
    });

    LAST_THREAD_SWITCH_NSEC.store(pit().nsec(), Ordering::Release);

    unsafe {
        asm_switch_thread(new_rsp);
    }

    Ok(())
}

pub fn create_thread(rip: usize, rsp: usize) -> KResult<()> {
    let kernel_stack = KernelStack::new()?;

    let stack_slice = unsafe { 
        slice::from_raw_parts_mut(
            kernel_stack.stack_base().as_mut_ptr(),
            kernel_stack.as_virt_range().size() / size_of::<usize>(),
        )
    };

    let mut push_index = 0;
    let mut push = |val: usize| {
        stack_slice[stack_slice.len() - 1 -push_index] = val;
        push_index += 1;
    };

    push(rsp);
    push(rip);
    push(asm_thread_init as usize);
    push(0);
    push(0);
    push(0);
    push(0);
    push(0);
    push(0);
    push(0x202);

    let kernel_rsp = kernel_stack.stack_top() - 8 * push_index;

    let thread = Thread::new(kernel_stack, kernel_rsp.as_usize());

    THREAD_MAP.insert_ready_thread(thread);

    Ok(())
}

pub fn init(stack: AVirtRange) -> KResult<()> {
    let thread = Thread::new(KernelStack::Existing(stack), 0);

    cpu_local_data().syscall_rsp.store(thread.syscall_rsp(), Ordering::Release);
    TSS.lock().rsp0 = thread.syscall_rsp() as u64;

    CURRENT_THREAD_HANDLE.store(thread.ptr_mut(), Ordering::Release);

    Ok(())
}