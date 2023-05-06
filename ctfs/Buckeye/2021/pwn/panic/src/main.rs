mod safe_map;
use safe_map::Store;
use std::panic::{self, AssertUnwindSafe};
use std::io::{self, Read, Write, BufRead};
use std::cmp::Ordering;

struct Account {
    full_name: String,
    balance: i64
}

impl Account {
    fn display(&self) {
        print!("Account {}: ", self.full_name);
        match self.balance.cmp(&0) {
            Ordering::Greater => println!("You owe ${}", self.balance),
            _ => println!("You are paid off!")
        }
    }

    fn pay(&mut self, amt: i64) {
        self.balance -= amt;
    }
}

macro_rules! could_panic {
    ($closure:tt) => {
        panic::catch_unwind(AssertUnwindSafe($closure));
    };
}

fn prompt() {
    print!("> ");
    io::stdout().flush().unwrap();
}

fn get_i64() -> Option<i64> {
    let mut input_text = String::new();
    io::stdin()
        .read_line(&mut input_text)
        .expect("failed to read from stdin");

    let trimmed = input_text.trim();

    trimmed.parse::<i64>().ok()
}

fn get_acct(accounts: &Store<String, Account>) -> Option<&Account> {
    let account_num = prompt_for("Please enter your account number: ")?;
    accounts.get(&account_num.trim().to_string())
}

fn get_acct_mut(accounts: &mut Store<String, Account>) -> Option<&mut Account> {
    let account_num = prompt_for("Please enter your account number: ")?;
    accounts.get_mut(&account_num.trim().to_string())
}

fn get_balance(accounts: &Store<String, Account>) {
    if let Some(acct) = get_acct(accounts) {
        acct.display();
    } else {
        println!("Could not find account.")
    }
}

fn make_payment(accounts: &mut Store<String, Account>) {
    if let Some(acct) = get_acct_mut(accounts) {
        print!("How much would you like to pay? ");
        io::stdout().flush().unwrap();
        if let Some(payment_amt) = get_i64() {
            acct.pay(payment_amt);
        } else {
            println!("Could not parse payment amount.");
        }
    } else {
        println!("Could not find account.")
    }
}

fn prompt_for(s: &str) -> Option<String> {
    let mut input = vec![];
    print!("{}", s);
    io::stdout().flush().unwrap();
    let stdin = io::stdin();
    let mut handle = stdin.lock();

    handle.read_until(b'\n', &mut input).ok()?;
    let input_s = String::from_utf8(input).ok()?;
    return Some(input_s.trim().to_string())
}

fn new_account(accounts: &mut Store<String, Account>) {
    if let (Some(acct_id), Some(full_name)) = (prompt_for("Account ID: "), prompt_for("Full Name: ")) {
        let result = could_panic!((|| {
            accounts.set(acct_id, Account { full_name: full_name.clone(), balance: 0 });
        }));
        match result {
            Err(_) => println!("Sorry, we couldn't open an account for you."),
            Ok(_) => println!("Welcome to <university name>, {}", full_name)
        }
    } else {
        println!("Could not read account name.");
    }
}

fn give_administrators_big_bonuses(accounts: &mut Store<String, Account>) {
    let result = could_panic!((|| {
        accounts.map_values(|_key, mut account: Account| -> Account {
            account.balance += 1000;
            account
        });
    }));

    match result {
        Err(_) => println!("Failed to give administrators large bonuses."),
        Ok(_) => println!("All is well")
    }
}

fn menu() {
    println!("1. Get balance");
    println!("2. Make Payment");
    println!("3. New Account");
    println!("4. Fund bonuses for administrators");
    println!("9. Exit");
}

fn main() {
    let mut accounts: Store<String, Account> = Store::new();
    println!("TUITION COLLECTION SYSTEM");
    println!("v0.5");
    println!("=========================");

    let mut input_buf: [u8; 2] =  [0; 2];

    loop {
        menu();
        prompt();
        
        io::stdin().read(&mut input_buf).expect("failed to read input.");
        let choice: i32 = std::str::from_utf8(&input_buf).unwrap().trim().parse().expect("invalid input");

        match choice {
            1 => { get_balance(&accounts) },
            2 => { make_payment(&mut accounts) },
            3 => { new_account(&mut accounts) },
            4 => { give_administrators_big_bonuses(&mut accounts) },
            9 => {
                println!("Bye!");
                return
                // process::exit(0);
            },
            _ => println!("Invalid choice!"),
        }
    }
}
