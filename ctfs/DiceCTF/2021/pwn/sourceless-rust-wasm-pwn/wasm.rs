use std::io;
use std::process;
use std::io::Write;
use std::io::Read;
use std::fs;
use std::ptr;
use std::str;

trait Sword {
    fn inspect(&mut self) -> String;
    fn display(&self) -> ();
}

struct RustySword {
    name: String,
}

impl Sword for RustySword {
    fn inspect(&mut self) -> String {
        return read_file();
    }

    fn display(&self) -> () {
        println!("Name: {}", self.name);
        println!("Description: {}", read_file());
    }
}

struct NewSword {
    name: String,
    desc: String,
}

impl Sword for NewSword {
    fn inspect(&mut self) -> String {
        println!("You inspect your handiwork.");
        println!("You admire its blade, and note something interesting.");
        prompt();
        let mut desc = String::new();
        io::stdin()
            .read_line(&mut desc)
            .expect("failed to read input.");
        self.desc = desc;
        return self.desc.clone();
    }

    fn display(&self) -> () {
        println!("Name: {}", self.name);
        println!("Description: {}", self.desc);
    }
}

fn menu() {
    println!("1. Forge a weapon");
    println!("2. Scrap a weapon");
    println!("3. Inspect a weapon");
    println!("4. View stock");
    println!("5. View log");
    println!("6. Exit");
}

fn forge<'a>(stock: &'a mut [*mut dyn Sword], c: &mut u8) -> &'a mut [*mut dyn Sword]  {
    let index: usize = (*c).into();

    println!("What's the name of your new weapon?");
    let mut new_name = String::new();
    prompt();
    io::stdin()
        .read_line(&mut new_name)
        .expect("failed to read input.");


    let new_weapon: Box<NewSword> = Box::new(NewSword {
        name: new_name,
        desc: String::from("None")
    });

    stock[index] = Box::into_raw(new_weapon) as *mut dyn Sword;
    *c += 1;
    println!("Done!");
    return stock;
}

fn scrap<'a>(stock: &'a mut [*mut dyn Sword], c: &mut u8) -> &'a mut [*mut dyn Sword]  {
    let index: usize = (*c).into();

    if index > 10 {
        // index-1 >= 10
        stock[index-1] = ptr::null_mut::<NewSword>();
        *c -= 1;
        println!("Done!");
    } else {
        println!("You feel yourself unable to scrap these legendary artifacts, rusty though they may be.");
    }
    return stock;
}

fn inspect<'a>(stock: &'a mut [*mut dyn Sword], log: &mut [u8]) -> &'a mut [*mut dyn Sword]  {
    println!("Which weapon do you want to inspect?");
    let mut index = String::new();
    prompt();
    io::stdin()
        .read_line(&mut index)
        .expect("failed to read input.");
    let index: usize = index.trim().parse().expect("invalid input");

    if !stock[index].is_null() {
        let log_s: String;
            let weapon: *mut dyn Sword = stock[index];
            unsafe {
                log_s = (*weapon).inspect();
            }

            if index >= 10 && log_s.len() > 256 {
                println!("Error: too big!");
                process::exit(0);
            }
            unsafe {
                ptr::copy_nonoverlapping(log_s.as_ptr(), log.as_mut_ptr(), log_s.len());
            }
    } else {
        println!("404 not found");
    }
    return stock;
}

fn view_stock<'a>(stock: &'a mut [*mut dyn Sword]) -> &'a mut [*mut dyn Sword]  {
    let mut index: usize = 0;

    while !stock[index].is_null() {
        let weapon: *mut dyn Sword = stock[index] as *mut dyn Sword;
        unsafe {
            (*weapon).display();
        }
        index += 1;
    }
    return stock;
}

fn view_log(log: &mut [u8]) {
    println!("You recall the weapon you saw last.");
    println!("{}", str::from_utf8(log).unwrap());
}

fn prompt() {
    print!("> ");
    io::stdout().flush().unwrap();
}

fn read_file() -> String {
    let src_file: &str = "excalibur.txt";
    let mut src_file_handle: fs::File = fs::File::open(&src_file).expect(&format!("Could not open file: {}", &src_file));
    let mut buf: String = String::new();
    src_file_handle.read_to_string(&mut buf)
        .expect(&format!("Failed to read data from file: {}", &src_file));
    return buf;
}

fn init_stock(stock: &mut [*mut dyn Sword]) -> &mut [*mut dyn Sword] {
    for i in 0..10 {
        let new_weapon: Box<RustySword> = Box::new(RustySword {
            name: format!("Excalibur {}", i+1),
        });

        stock[i] = Box::into_raw(new_weapon) as *mut dyn Sword;
    }
    return stock;
}

fn main() {
    let mut stock: [*mut dyn Sword; 256] = [ptr::null_mut::<NewSword>(); 256];
    let mut c: u8 = 10;
    let mut stock_ptr: &mut [*mut dyn Sword] = &mut stock;
    let mut input_buf: [u8; 2] =  [0; 2];
    let mut log: [u8; 256] = [0; 256];

    stock_ptr = init_stock(stock_ptr);

    println!("You are a blacksmith who has recently been exiled from your home. You leave, reluctant to part with your bustling shop with all your hard-forged equipment.");
    println!("As you travel across distant lands, you stumble upon a town. In it, you find an abandoned armory. Though all the equipment is rusted over, you decide to rennovate it and reestablish your bustling blacksmithing empire.");
    println!("This is your story of how you went from a scorned, penniless blacksmith to, well, a scorned, penniless blacksmith with a flag.");

    loop {
        menu();
        prompt();
        io::stdin().read(&mut input_buf).expect("failed to read input.");
        let choice: i32 = std::str::from_utf8(&input_buf).unwrap().trim().parse().expect("invalid input");

        match choice {
            1 => { stock_ptr = forge(stock_ptr, &mut c) },
            2 => { stock_ptr = scrap(stock_ptr, &mut c) },
            3 => { stock_ptr = inspect(stock_ptr, &mut log) },
            4 => { stock_ptr = view_stock(stock_ptr) },
            5 => view_log(&mut log),
            6 => {
                println!("Bye!");
                process::exit(0);
            },
            _ => println!("Invalid choice!"),
        }
    }
}