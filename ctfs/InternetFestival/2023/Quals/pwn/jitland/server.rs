extern crate solana_rbpf;

use solana_rbpf::{
    aligned_memory::AlignedMemory,
    ebpf,
    elf::Executable,
    memory_region::{MemoryMapping, MemoryRegion},
    verifier::{RequisiteVerifier, TautologyVerifier},
    vm::{BuiltInProgram, Config, EbpfVm, FunctionRegistry, TestContextObject, ProgramResult},
    syscalls::{bpf_trace_printf, bpf_gather_bytes, bpf_mem_frob, bpf_str_cmp, bpf_syscall_string, bpf_syscall_u64}
};
use std::io::{self, Write};
use syscalls::{raw_syscall, Sysno};
use hex;

const SHOULD_JITCOMPILE: bool = true;

fn get_config() -> Config {
    let mut inp = String::new();
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut inp).unwrap();
    let input_blob = hex::decode(inp.trim()).unwrap();
    if input_blob.len() != std::mem::size_of::<Config>() {
        panic!("Invalid Config size");
    }
    let mut buf: [u8; std::mem::size_of::<Config>()] = [0; std::mem::size_of::<Config>()];
    buf.copy_from_slice(input_blob.as_slice());
    unsafe { std::mem::transmute_copy(&buf) }
}

fn get_blob() -> Vec<u8> {
    let mut inp = String::new();
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut inp).unwrap();
    hex::decode(inp.trim()).unwrap()
}


pub fn bpf_syscall_write(
    _context_object: &mut TestContextObject,
    arg1: u64,
    arg2: u64,
    arg3: u64,
    _arg4: u64,
    _arg5: u64,
    _memory_mapping: &mut MemoryMapping,
    result: &mut ProgramResult,
) {
    let rv = unsafe {
        raw_syscall!(
            Sysno::write,
            arg1,
            arg2,
            arg3
        )
    };
    *result = ProgramResult::Ok(rv as u64);
}

fn syscall_pipe(
    pipe_arr: &mut [i32; 2]
) -> usize {
    let rv = unsafe {
        raw_syscall!(
            Sysno::pipe,
            pipe_arr.as_mut_ptr()
        )
    };
    rv
}

fn main() {
    print!("Enter your program as a hex string: ");
    let prog = &get_blob()[..];
    print!("Enter your program memory as a hex string: ");
    let mem = &mut get_blob()[..];
    print!("Enter your program config as a hex string: ");
    let config = get_config();
    let mut loader: BuiltInProgram<TestContextObject> = BuiltInProgram::new_loader(config);
    loader.register_function(b"write", bpf_syscall_write as _).unwrap();
    loader.register_function(b"trace_printf", bpf_trace_printf as _).unwrap();
    loader.register_function(b"gather_bytes", bpf_gather_bytes as _).unwrap();
    loader.register_function(b"mem_frob", bpf_mem_frob as _).unwrap();
    loader.register_function(b"str_cmp", bpf_str_cmp as _).unwrap();
    loader.register_function(b"syscall_string", bpf_syscall_string as _).unwrap();
    loader.register_function(b"syscall_u64", bpf_syscall_u64 as _).unwrap();

    let loader = std::sync::Arc::new(loader);
    let function_registry = FunctionRegistry::default();
    let executable =
        Executable::<TautologyVerifier, TestContextObject>::new_from_text_bytes(prog, loader, function_registry).unwrap();
    let mut verified_executable = Executable::<RequisiteVerifier, TestContextObject>::verified(executable).unwrap();
    if SHOULD_JITCOMPILE {
        verified_executable.jit_compile().unwrap();
    }
    let mut context_object = TestContextObject::new(100);
    let config = verified_executable.get_config();

    let mut stack = AlignedMemory::<{ ebpf::HOST_ALIGN }>::zero_filled(config.stack_size());
    let stack_len = stack.len();
    let mut heap = AlignedMemory::<{ ebpf::HOST_ALIGN }>::with_capacity(0);

    let regions: Vec<MemoryRegion> = vec![
        verified_executable.get_ro_region(),
        MemoryRegion::new_writable_gapped(
            stack.as_slice_mut(),
            ebpf::MM_STACK_START,
            if !config.dynamic_stack_frames && config.enable_stack_frame_gaps {
                config.stack_frame_size as u64
            } else {
                0
            },
        ),
        MemoryRegion::new_writable(heap.as_slice_mut(), ebpf::MM_HEAP_START),
        MemoryRegion::new_writable(mem, ebpf::MM_INPUT_START),
    ];

    let memory_mapping = MemoryMapping::new(regions, config).unwrap();

    let mut vm = EbpfVm::new(
        &verified_executable,
        &mut context_object,
        memory_mapping,
        stack_len,
    );
    
    // Create a pipe for the ebpf program to write to
    let mut pipe_arr: [i32; 2] = [0; 2];
    syscall_pipe(&mut pipe_arr);
    println!("Created a new pipe: {:?}", pipe_arr);

    // Set pipe non blocking so that the read syscall doesn't block
    let old_flags = unsafe {
        raw_syscall!(
            Sysno::fcntl,
            pipe_arr[0],
            0x3 // F_GETFL   
        )
    }; 
    unsafe {
        raw_syscall!(
            Sysno::fcntl,
            pipe_arr[0],
            0x4, // F_SETFL
            old_flags | 0x800 // O_NONBLOCK
        )
    };
    
    let (_instruction_count, result) = vm.execute_program(!SHOULD_JITCOMPILE);
    println!("result: {:?}", result);
    println!("context_object: {:?}", context_object);
    
    // Read output from ebpf program
    let mut buf: [u8; 100] = [0x41; 100];
    let rv = unsafe {
        raw_syscall!(
            Sysno::read,
            pipe_arr[0],
            buf.as_mut_ptr() as u64,
            100
        )
    };
    let sz = if rv > 100 { 0 } else { rv as usize };
    println!("read({:#x}, {:?}, {:#x}) = {:#x}", pipe_arr[0], &buf[..sz], 100, rv);
    
}
