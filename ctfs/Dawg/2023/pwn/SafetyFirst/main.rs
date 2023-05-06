use std::io;
use std::io::Write;

fn main() -> io::Result<()> {
    println!("Welcome to my 🚀 BLAZING FAST 🚀 caesar cipher program.");
    print!("Enter your input: ");
    io::stdout().flush()?;
    let mut input = String::new();
    io::stdin().read_line(&mut input)?;
    println!("Original input was {}", input);

    let mut buffer: [u8; 64] = [0; 64];
    let mut admin_mode: u32 = 0;

    unsafe {
        core::ptr::write_volatile(&mut admin_mode as *mut u32, 0);
        std::ptr::copy(input.as_ptr(), buffer.as_mut_ptr(), input.len());
        for i in 0..input.len() {
            *(buffer.as_mut_ptr().offset(i as isize)) += 13;
        }
    }

    println!("Result:");
    std::io::stdout().write(&buffer)?;
    println!("");
    println!("Done!");

    if admin_mode == 0x71726e71 {
        let flag = std::fs::read_to_string("flag.txt")?;
        println!("Flag is {}", flag);
    }

    Ok(())
}
