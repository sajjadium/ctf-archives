#![feature(asm)]
use std::ptr;
use std::mem;
use std::io::{self, Write};

type Element = Vec<i32>;
type List = [Element; 10];

macro_rules! CHECK_BOUNDS {
    ($list:expr, $index:expr) => {
        if $index >= $list.len() {
            println!("[-] Invalid index");
            return;
        }
    };
}

static mut IS_SWAP_USED: bool = false;

fn read_str(msg: &str) -> String {
    let mut s = String::new();
    print!("{}", msg);
    io::stdout().flush().expect("I/O Error");
    io::stdin().read_line(&mut s).expect("I/O Error");
    String::from(s.trim())
}

fn read_i32(msg: &str) -> i32 {
    read_str(msg).parse().expect("Invalid input")
}

fn menu() -> i32 {
    println!("+-----------+");
    println!("| 1. set    |");
    println!("| 2. show   |");
    println!("| 3. swap   |");
    println!("+-----------+");
    read_i32(">> ")
}

fn val_set(list: &mut List) {
    let index = read_i32("index: ") as usize;
    CHECK_BOUNDS!(list, index);
    let size = read_i32("size: ") as usize;
    list[index] = Vec::with_capacity(size);
    for i in 0..size {
        list[index].push(read_i32(&format!("elements[{}] = ", i)));
    }
}

fn val_show(list: &mut List) {
    for i in 0..list.len() {
        if !list[i].is_empty() {
            println!("{}: {:?}", i, list[i]);
        }
    }
}

fn val_swap(list: &mut List) {
    unsafe {
        if IS_SWAP_USED {
            println!("[-] You can use this function only once");
            return;
        } else {
            IS_SWAP_USED = true;
        }
    }

    let index_1 = read_i32("index 1: ") as usize;
    let index_2 = read_i32("index 2: ") as usize;

    /* https://stackoverflow.com/a/31213780 */
    unsafe {
        let s = mem::MaybeUninit::zeroed();
        let mut t: Element = s.assume_init();
        CHECK_BOUNDS!(list, index_1);
        ptr::copy_nonoverlapping(&list[index_1], &mut t, 1);
        CHECK_BOUNDS!(list, index_2);
        ptr::copy_nonoverlapping(&list[index_2], &mut list[index_1], 1);
        ptr::copy_nonoverlapping(&t, &mut list[index_2], 1);
        mem::forget(t);
    }
}

fn main() {
    let _cleanup = Cleanup{};
    let mut list: List = Default::default();
    loop {
        match menu() {
            1 => val_set(&mut list),
            2 => val_show(&mut list),
            3 => val_swap(&mut list),
            _ => {
                println!("[+] Bye (^q^)ﾉｼ");
                break;
            }
        }
    }
}

struct Cleanup;
impl Drop for Cleanup {
    fn drop(&mut self) {
        // Kill myself without cleanup
        unsafe {
            asm!(
                "xor edi, edi",
                "mov eax, 60",
                "syscall"
            );
        }
    }
}
