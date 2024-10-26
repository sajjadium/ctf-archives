use std::ptr;
use std::fs;
use std::io::{self, Write};
use std::alloc::{alloc, dealloc, Layout};

struct BankAccount {
    balance: i32,
    deposits: u32,
}

impl BankAccount {
    unsafe fn new() -> *mut BankAccount {
        let layout = Layout::new::<BankAccount>();
        let ptr = alloc(layout) as *mut BankAccount;

        if ptr.is_null() {
            panic!("Memory allocation failed!");
        }

        (*ptr).deposits = 0;
        ptr 
    }

    unsafe fn deposit(account: *mut BankAccount) {
        if (*account).deposits >= 13 {
            println!("Deposit limit reached this month.");
            return;
        }

        print!("How much do you want to deposit? ");
        io::stdout().flush().unwrap();
        let mut amount_input = String::new();
        io::stdin().read_line(&mut amount_input).unwrap();
        let amount: i32 = amount_input.trim().parse().unwrap();

        if amount < 0 {
            return;
        } else if amount > 100 {
            println!("You cannot exceed 100 per deposit.");
            return;
        } else {
            (*account).balance += amount;
            (*account).deposits += 1;
        }
        
    }

    unsafe fn withdraw(account: *mut BankAccount) {
        print!("How much do you want to withdraw? ");
        io::stdout().flush().unwrap();
        let mut amount_input = String::new();
        io::stdin().read_line(&mut amount_input).unwrap();
        let amount: i32 = amount_input.trim().parse().unwrap();

        if (amount < 0) {
            return;
        } else if amount > (*account).balance {
            println!("Insufficient funds.");
            return;
        } else {
            (*account).balance -= amount;
        }
    }

}

unsafe fn menu() {
    println!("1) Insert BankRupst card");
    println!("2) Deposit");
    println!("3) Withdraw");
    println!("4) Check Balance");
    println!("5) Remove BankRupst card");
    println!("6) Exit");
}

fn main() {

    unsafe {
        let mut account: *mut BankAccount = ptr::null_mut();
        let mut opened: bool = false;

        println!("Welcome in BankRupst!");
        println!("We're a bank operating in bankruptcy where there are no laws governing our operations.");

        loop{
            menu();
            print!("Choose an option: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            io::stdin().read_line(&mut input).unwrap();
            let choice: i32 = input.trim().parse().unwrap_or(0);

            match choice {
                1 => {
                    if !opened {
                        account = BankAccount::new();
                        opened = true;
                        println!("BankRupst card inserted");
                    } else {
                        println!("You already inserted your BankRupst card!");
                    }
                }
                2 => {
                    if opened {
                        BankAccount::deposit(account);
                    } else {
                        println!("Enter your BankRupst card!");
                    }
                }
                3 => {
                    if opened {
                        BankAccount::withdraw(account);
                    } else {
                        println!("Enter your BankRupst card!");
                    }
                }
                4 => {
                    if opened {
                        println!("Account balance: {}", (*account).balance);
                        if (*account).balance > 1337 {
                            println!("Congrats! You are now a special member!");
                            let flag_file = "flag.txt";
                            match fs::read_to_string(flag_file) {
                                Ok(flag) => println!("{}", flag),
                                Err(e) => eprintln!("Error reading flag.txt: {}", e),
                            }
                        }
                    } else {
                        println!("Enter your BankRupst card!");
                    }

                }
                5 => {
                    if opened {
                        (*account).balance=0;
                        (*account).deposits = 0;
                        ptr::drop_in_place(account);
                        opened = false;
                        println!("BankRupst card removed.");
                    } else {
                        println!("You must insert your BankRupst card!");
                    }
                }
                6 => {
                    if opened {
                        (*account).balance=0;
                        (*account).deposits = 0;
                        let layout = Layout::new::<BankAccount>();
                        dealloc(account as *mut u8, layout);
                        account = ptr::null_mut();
                        opened = false;
                        println!("Thank you for using BankRupst!");
                    } else {
                        println!("Thank you for using BankRupst!");
                        break;
                    }

                }
                _ => println!("Invalid option.")
            }
        }

    }
}
