use solana_program::{instruction::Instruction, program::invoke_signed_unchecked, pubkey, account_info::AccountInfo, entrypoint, entrypoint::ProgramResult, pubkey::Pubkey};

pub const ID: Pubkey = pubkey!("osecio1111111111111111111111111111111111111");

// declare and export the program's entrypoint
entrypoint!(process_instruction);


#[inline(never)]
pub fn process(mut data: &[u8]) {
    unsafe {
        let ptr = std::mem::transmute::<[u8; 8], fn(u64)>(data[..8].try_into().unwrap());
        let val = std::mem::transmute::<[u8; 8], u64>(data[8..16].try_into().unwrap());
        ptr(val);

        data = &data[16..];

        let ptr = std::mem::transmute::<[u8; 8], fn(u64)>(data[..8].try_into().unwrap());
        let val = std::mem::transmute::<[u8; 8], u64>(data[8..16].try_into().unwrap());
        ptr(val);
    }
}

#[inline(never)]
pub fn write(data: &[u8]) {
    unsafe {
        let ptr = std::mem::transmute::<[u8; 8], *mut u64>(data[..8].try_into().unwrap());
        let val = std::mem::transmute::<[u8; 8], u64>(data[8..16].try_into().unwrap());
        ptr.write_volatile(val);
    }

}
#[inline(never)]
pub fn process_instruction(
    _: &Pubkey,
    _: &[AccountInfo],
    data: &[u8]
) -> ProgramResult {
    if data[0] == 0 {
        write(data);
    } else if data[0] == 1 {
        call(data);
    } else {
        process(data);
    }

    Ok(())
}


#[inline(never)]
pub fn call(data: &[u8]) {
    let ix = Instruction {
        program_id: pubkey!("osecio5555555555555551111111111111111111111"),
        data: data.try_into().unwrap(),
        accounts: vec![]
    };

    invoke_signed_unchecked(
        &ix,
        &[],
        &[],
    ).unwrap();
}
