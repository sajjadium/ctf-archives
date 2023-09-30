extern crate libc;
use crate::arm64::*;
use std::{
    ptr,
    mem
};
pub struct VM {
    text_section: &'static mut [u8],
    stack: &'static mut [u8],
    text_size: usize,
    cur_text_offset: usize,
    stack_slots: usize
}

const VM_STACK_POINTER: u8 = X4;
const VM_STACK_BOTTOM: u8 = X5;
const VM_STACK_SIZE: usize = 0x8000;

#[inline]
pub fn emit<T>(vm: &mut VM, data: T) {
    if vm.cur_text_offset + mem::size_of::<T>() > vm.text_size {
        panic!("Ran out of text space");
    }
    unsafe {
        let ptr = vm.text_section.as_ptr().add(vm.cur_text_offset);
        ptr::write_unaligned(ptr as *mut T, data as T);
    }
    vm.cur_text_offset += mem::size_of::<T>();
}

fn round_to_page_size(size: usize, page_size: usize) -> usize {
    (size + (page_size-1)) & (!(page_size-1))
}

impl VM {
    pub fn new(code_size: usize) -> Self {
        unsafe {
            let page_size = libc::sysconf(libc::_SC_PAGESIZE) as usize;
            let over_allocated_code_size = round_to_page_size(code_size, page_size);
            let mut code_raw: *mut libc::c_void = std::ptr::null_mut();
            let mut stack_raw: *mut libc::c_void = std::ptr::null_mut();
            code_raw = libc::mmap(code_raw, over_allocated_code_size, libc::PROT_READ | libc::PROT_WRITE, libc::MAP_ANONYMOUS | libc::MAP_PRIVATE, 0, 0);
            stack_raw = libc::mmap(stack_raw, VM_STACK_SIZE, libc::PROT_READ | libc::PROT_WRITE, libc::MAP_ANONYMOUS | libc::MAP_PRIVATE, 0, 0);
            if code_raw.is_null() || stack_raw.is_null() {
                panic!("Could not mmap code and stack")
            }
            Self {
                text_section: std::slice::from_raw_parts_mut(code_raw as *mut u8, code_size),
                stack: std::slice::from_raw_parts_mut(stack_raw as *mut u8, VM_STACK_SIZE),
                text_size: over_allocated_code_size,
                cur_text_offset: 0,
                stack_slots: VM_STACK_SIZE / 8
            }
        }
    }

    #[inline]
    fn emit_pop(&mut self, reg: u8) {
        ARM64Instruction::load(OperandSize::S64, VM_STACK_POINTER, ARM64MemoryOperand::OffsetPostIndex(-8), reg).emit(self);
    }

    #[inline]
    fn emit_push(&mut self, reg: u8) {
        ARM64Instruction::store(OperandSize::S64, reg, VM_STACK_POINTER, ARM64MemoryOperand::OffsetPreIndex(8)).emit(self);
    }

    #[inline]
    fn emit_load_immediate64(&mut self, reg: u8, mut imm: u64) {
        ARM64Instruction::mov(OperandSize::S64, SP_XZR, reg).emit(self);

        let mut shift: u8 = 0;
        while imm != 0 {
            ARM64Instruction::movk(reg, shift, imm as u16).emit(self);
            imm >>= 16;
            shift += 1;
        }
    }

    fn emit_stack_off_check(&mut self, reg: u8) {
        ARM64Instruction::sub(OperandSize::S64, VM_STACK_POINTER, VM_STACK_BOTTOM, X2).emit(self);
        ARM64Instruction::cmp(OperandSize::S64, reg, X2).emit(self);
        ARM64Instruction::b_cond(Condition::HI, 3).emit(self);
        ARM64Instruction::mvn(OperandSize::S64, SP_XZR, X0).emit(self);
        ARM64Instruction::ret().emit(self);
    }

    fn emit_prologue(&mut self) {
        ARM64Instruction::mov(OperandSize::S64, X0, VM_STACK_POINTER).emit(self);
        ARM64Instruction::mov(OperandSize::S64, X0, VM_STACK_BOTTOM).emit(self);
        ARM64Instruction::store(OperandSize::S64, X1, VM_STACK_POINTER, ARM64MemoryOperand::OffsetPreIndex(0)).emit(self);
    }

    pub fn compile(&mut self, code: &[u8]) {
        let mut pc: usize = 0;
        let mut sp = 0;
        self.emit_prologue();
        while pc < code.len() {
            let opc = code[pc];
            pc += 1;
            match opc {
                0 => {},
                1 | 2 | 3 | 4 | 5 => {
                    assert!(sp >= 2);
                    sp -= 1;
                    self.emit_pop(X0);
                    self.emit_pop(X1);
                    match opc {
                        1 => ARM64Instruction::add(OperandSize::S64, X0, X1, X0).emit(self),
                        2 => ARM64Instruction::sub(OperandSize::S64, X0, X1, X0).emit(self),
                        3 => ARM64Instruction::eor(OperandSize::S64, X1, X0).emit(self),
                        4 => ARM64Instruction::lsl_reg(OperandSize::S64, X0, X1, X0).emit(self),
                        5 => ARM64Instruction::lsr_reg(OperandSize::S64, X0, X1, X0).emit(self),
                        _ => unreachable!()
                    }
                    self.emit_push(X0);
                },
                6 => {
                    assert!(sp < self.stack_slots);
                    sp += 1;
                    let imm: u64 = unsafe {
                        let ptr = code.as_ptr().add(pc);
                        ptr::read_unaligned(ptr as *const u64)
                    };
                    pc += 8;
                    self.emit_load_immediate64(X0, imm);
                    self.emit_push(X0);
                },
                7 => {
                    assert!(sp < self.stack_slots);
                    sp += 1;
                    ARM64Instruction::load(OperandSize::S64, VM_STACK_POINTER, ARM64MemoryOperand::OffsetPreIndex(0), X0).emit(self);
                    self.emit_push(X0);
                },
                8 => {
                    assert!(sp >= 1);
                    self.emit_pop(X0);
                    self.emit_stack_off_check(X0);
                    ARM64Instruction::sub(OperandSize::S64, SP_XZR, X0, X0).emit(self);
                    ARM64Instruction::load(OperandSize::S64, VM_STACK_POINTER, ARM64MemoryOperand::OffsetIndex(X0), X0).emit(self);
                    self.emit_push(X0);
                },
                9 => {
                    assert!(sp >= 2);
                    sp -= 2;
                    self.emit_pop(X0);
                    self.emit_pop(X1);
                    self.emit_stack_off_check(X0);
                    ARM64Instruction::sub(OperandSize::S64, SP_XZR, X0, X0).emit(self);
                    ARM64Instruction::store(OperandSize::S64, X1, VM_STACK_POINTER, ARM64MemoryOperand::OffsetIndex(X0)).emit(self);
                },
                10 => {
                    assert!(sp >= 1);
                    ARM64Instruction::ret().emit(self);
                },
                _ => {
                    panic!("Invalid opcode {}", opc);
                }
            }
        }
        ARM64Instruction::mvn(OperandSize::S64, SP_XZR, X0).emit(self);
        ARM64Instruction::ret().emit(self);
    }

    pub fn execute(&mut self, input: u64) -> i64 {
        if unsafe { libc::mprotect(self.text_section.as_mut_ptr() as *mut _, self.text_size, libc::PROT_EXEC | libc::PROT_READ) } != 0 {
            panic!("mprotect failed");
        }
        let code: fn(*mut u8, u64) -> i64 = unsafe { std::mem::transmute(self.text_section.as_ptr()) };
        let result = code(self.stack.as_mut_ptr(), input);
        return result;
    }
}
