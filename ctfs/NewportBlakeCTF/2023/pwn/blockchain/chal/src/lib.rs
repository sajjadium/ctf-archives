use solana_rbpf::elf::Executable;
use solana_rbpf::program::{BuiltinFunction, BuiltinProgram, FunctionRegistry, SBPFVersion};
use solana_rbpf::vm::{Config, EbpfVm, TestContextObject};
use solana_rbpf::verifier::RequisiteVerifier;
use solana_rbpf::ebpf;
use solana_rbpf::memory_region::{MemoryRegion, MemoryMapping};
use std::sync::Arc;

const STACK_LEN: usize = 0x4000;

#[no_mangle]
extern "C" fn challenge(data: *mut u8, len: usize) {
    let data: &mut [u8] = unsafe { std::slice::from_raw_parts_mut(data, len) };
    match blockchain(data) {
        Err(e) => println!("challenge errored with: {e}"),
        Ok(_) => println!("done!"),
    }
}

fn blockchain(data: &mut [u8]) -> Result<(), Box<dyn std::error::Error>> {
    let mut stack: [u8; STACK_LEN] = [0; STACK_LEN];
    let sbpf_version = SBPFVersion::V2;

    let mut config = Config::default();
    config.new_elf_parser = true;
    config.enable_sbpf_v2 = true;
    config.enable_sbpf_v1 = true;
    config.noop_instruction_rate = 0;
    config.sanitize_user_provided_values = false;
    config.reject_broken_elfs = true;
    config.reject_callx_r10 = true;

    let result = FunctionRegistry::<BuiltinFunction<TestContextObject>>::default();
    let program = BuiltinProgram::new_loader(config, result);
    let loader = Arc::new(program);

    let mut executable = Executable::load(data, loader.clone())?;
    executable.verify::<RequisiteVerifier>()?;
    executable.jit_compile()?;

    let regions: Vec<MemoryRegion> = vec![
        executable.get_ro_region(),
        MemoryRegion::new_writable_gapped(&mut stack, ebpf::MM_STACK_START, 0),
    ];
    let memory_mapping = MemoryMapping::new(regions, &config, &sbpf_version)?;

    let mut ctx = TestContextObject::new(100000);

    let mut vm = EbpfVm::new(loader.clone(), &sbpf_version, &mut ctx, memory_mapping, STACK_LEN);
    let (_, res) = vm.execute_program(&executable, false);

    println!("exited with: {res:?}.");

    Ok(())
}
