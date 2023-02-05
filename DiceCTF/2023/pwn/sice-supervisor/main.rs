use std::{io::{self, Write, Read}, process::{self, Command, Stdio}, str, thread};
use std::sync::mpsc;

use regex::bytes::Regex;

fn menu() {
  println!("1. Deploy a deet daemon");
  println!("2. Sice a deet daemon");
  println!("3. Filter a deet daemon");
  println!("4. Exit");
}

fn prompt() {
    print!("> ");
    io::stdout().flush().unwrap();
}

fn main() {
  let mut deet_daemons = Vec::new();
  let mut deet_daemon_chans = Vec::new();
  let mut choice_buf: [u8; 2] =  [0; 2];
  let mut input_buf: [u8; 1000] =  [0; 1000];

  println!("Sice Supervisor");

  loop {
    menu();
    prompt();
    io::stdin().read(&mut choice_buf).expect("failed to read input.");
    let choice: i32 = std::str::from_utf8(&choice_buf).unwrap().trim().parse().expect("invalid input");

    match choice {
      1 => {

        let (sender, receiver) = mpsc::channel();

        let mut child = Command::new("./deet_daemon")
          .stdin(Stdio::piped())
          .stdout(Stdio::piped())
          .spawn()
          .expect("failed to deploy a deet daemon");
        
        let stdin = child.stdin.take().expect("failed to open stdin");
        let mut stdout = child.stdout.take().expect("failed to open stdout");
        thread::spawn(move || { 
          let mut input_buf: [u8; 100000] = [0; 100000];
          loop {
            let filter = receiver.try_recv().ok().map(|s: String| Regex::new(s.as_str()).expect("failed to create filter"));

            let sz = stdout.read(&mut input_buf).expect("failed to read deet");
            if sz > 0 && filter.filter(|f| !f.is_match(&input_buf[..sz])).is_none() {
              io::stdout().write_all(&input_buf[..sz]).expect("failed to write to stdout");
              io::stdout().flush().expect("failed to flush stdout");
            }
          }
        });
        deet_daemons.push(stdin);
        deet_daemon_chans.push(sender);
        println!("Created deet {}", deet_daemons.len() - 1);
      },
      2 => {
        println!("Which deet daemon do you want to sice?");
        prompt();
        io::stdin().read(&mut choice_buf).expect("failed to read input.");
        let choice: usize = std::str::from_utf8(&choice_buf).unwrap().trim().parse().expect("invalid input");
        let deet = &mut deet_daemons[choice];
        println!("What do you want to sice?");
        prompt();
        let sz = io::stdin().read(&mut input_buf).expect("failed to read input");
        deet.write_all(&input_buf[..sz]).expect("failed to sice deet");
      },
      3 => {
        println!("Which deet daemon do you want to filter?");
        prompt();
        io::stdin().read(&mut choice_buf).expect("failed to read input.");
        let choice: usize = std::str::from_utf8(&choice_buf).unwrap().trim().parse().expect("invalid input");

        println!("What's your filter?");
        prompt();
        let sz = io::stdin().read(&mut input_buf).expect("failed to read input");
        let filter = str::from_utf8(&input_buf[..sz]).expect("failed to convert input to string").to_string();

        deet_daemon_chans[choice].send(filter).expect("failed to send filter");
      },
      4 => {
        println!("you will not be missed");
        process::exit(0);
      },
      _ => println!("Invalid choice!"),
    }
  }
}
