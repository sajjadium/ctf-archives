use core::panic::PanicInfo;

#[panic_handler]
fn panic(info: &PanicInfo) -> ! {
    crate::println!("{}", info);
    exit();
}

pub fn exit() -> ! {
    unsafe {
        asm!(
            "bkpt #0xab",
            in("r1") 0x20026, 
            inout("r0") 0x18 => _,
        );
    }
    
    loop {}
}

#[repr(C)]
struct SemihostingOpenParams {
     device_name: *const u8,
     mode: u32,
     name_length: u32,
}

#[repr(C)]
struct SemihostingReadParams {
     handle: i32,
     buffer: *const u8,
     length_to_read: u32,
}

const FILENAME: &[u8; 9] = b"flag.txt\0";
const CONTENTS_LEN: u32 = 23;

const SEEDREAD: SemihostingOpenParams = SemihostingOpenParams {
    device_name: FILENAME.as_ptr(),
    mode: 0,
    name_length: FILENAME.len() as u32 - 1
};

pub fn dump_flag() {
    let mut handle = 0i32;
    // Open file
    unsafe {
            asm!(
                "bkpt #0xab",
                in("r1") &SEEDREAD as *const SemihostingOpenParams as *const u32,
                inout("r0") 0x01 => handle,
            );
    }
    if handle == -1 {
        return;
    }
    // read it
    let buffer = [0u8; 32];
    let read_params = SemihostingReadParams {
        handle: handle,
        buffer: buffer.as_ptr(),
        length_to_read: CONTENTS_LEN 
    };
    let mut ret = 0;
    unsafe {
            asm!(
                "bkpt #0xab",
                in("r1") &read_params as *const SemihostingReadParams as *const u32,
                inout("r0") 0x06 => ret,
            );
    }
    if ret != 0 {
        return;
    }

    crate::println!("{}", core::str::from_utf8(&buffer).unwrap());

    // close file
    unsafe {
            asm!(
                "bkpt #0xab",
                in("r1") &handle,
                inout("r0") 0x02 => ret,
            );
    }
}