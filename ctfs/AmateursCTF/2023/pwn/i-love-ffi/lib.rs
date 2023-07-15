#![allow(warnings)]

pub struct MmapArgs {
    addr: u64,
    length: u64,
    protection: u32,
    flags: u32,
    fd: u32,
    offset: u64,
}

#[no_mangle]
pub extern "C" fn mmap_args() -> MmapArgs {
    let args = MmapArgs {
        addr: read::<u64>(),
        length: read::<u64>(),
        protection: read::<u32>(),
        flags: read::<u32>(),
        fd: read::<u32>(),
        offset: read::<u64>(),
    };

    if args.protection & 4 != 0 {
        panic!("PROT_EXEC not allowed");
    }

    args
}

fn read<T>() -> T
where
    T: std::str::FromStr,
    <T as std::str::FromStr>::Err: std::fmt::Debug,
{
    use std::io::{stdin, stdout, Write};
    print!("> ");
    stdout().flush().unwrap();
    let mut buf = String::new();
    stdin().read_line(&mut buf).unwrap();
    buf.trim().parse::<T>().unwrap()
}
