use std::io::{self, Write, Read};
use dns_lookup::{lookup_host, lookup_addr};
use std::net::Ipv4Addr;
use std::process::Command;
use std::str;
use std::string::String;

static mut CHOICE: i32 = 0;

fn read(arr: &mut[u8], size: isize) -> isize{
    let arr_ptr = &mut arr[0] as *mut u8;
    let mut count = 0;
    unsafe{
        let mut input: [u8;1] = [0;1];
        for i in 0..size {
            io::stdin().read_exact(&mut input).expect("msg");
            if input[0] == 0xa {
                break;
            }
            *arr_ptr.offset(i) = input[0];
        }

        while *arr_ptr.offset(count) != 0{
            count+=1;
        }
    }
    count
}

fn menu(){
    println!("1. ping");
    println!("2. traceroute");
    println!("3. IP lookup");
    println!("4. Reverse IP lookup");
    println!("5. Exit");
    print!("> ");
    io::stdout().flush().unwrap();
}

fn ping(){
    let mut input: String = String::new();
    print!("IPv4: ");
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut input).expect("Failed to read IP");
    match input.trim().parse::<Ipv4Addr>() {
        Ok(ip) => {
            let cmd = format!("ping {} -w 4", ip.to_string());
            let process = Command::new("/bin/sh")
                                .arg("-c")
                                .arg(cmd)
                                .output()
                                .expect("Failed");
            println!("{}", String::from_utf8_lossy(&process.stdout));
        }
        _ => {
            println!("Invalid IPv4 format!");
            return;
        },
    };
}

fn traceroute(){
    let mut input: String = String::new();
    print!("IPv4: ");
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut input).expect("Failed to read IP");
    match input.trim().parse::<Ipv4Addr>() {
        Ok(ip) => {
            let cmd = format!("traceroute {}", ip.to_string());
            let process = Command::new("/bin/sh")
                                .arg("-c")
                                .arg(cmd)
                                .output()
                                .expect("Failed");
            println!("{}", String::from_utf8_lossy(&process.stdout));
        }
        _ => {
            println!("Invalid IPv4 format!");
            return;
        },
    };
}

fn ip_lookup(){
    let mut input: [u8; 400] = [0; 400];

    print!("Hostname: ");
    io::stdout().flush().unwrap();
    let size = read(&mut input, 0x400);
    let (hostname, _) = input.split_at(size as usize);
    let hostname = str::from_utf8(hostname).expect("msg").to_string();
    // println!("{:?}", hostname.trim());
    match lookup_host(hostname.trim()) {
        Ok(ip) => println!("{:?}", ip),
        _ => println!("Invalid domain name!")
    }
}

fn reverse_ip_lookup(){
    let mut ip_str: String = String::new();

    print!("IP: ");
    io::stdout().flush().unwrap();
    io::stdin().read_line(&mut ip_str).expect("Failed to read IP");
    
    match ip_str.trim().parse::<std::net::IpAddr>() {
        Ok(ip) => {
            match lookup_addr(&ip) {
                Ok(hostname) => println!("{}", hostname),
                _ => println!("Invalid IP!")
            }
        },
        _ => {
            println!("Invalid IP format!");
            return;
        }
    }
}

fn main(){
    unsafe {
        let mut input = String::new();

        println!("**************************");
        println!("*                        *");
        println!("*     Network Tools      *");
        println!("*                        *");
        println!("**************************");
        println!("Opss! Something is leaked: {:p}", &CHOICE);
        loop {
            menu();

            input.clear();
            io::stdin().read_line(&mut input).expect("Failed to readline!");
            CHOICE = match input.trim().parse() {
                Ok(num) => num,
                _ => 0
            };
            match CHOICE {
                1 => ping(),
                2 => traceroute(),
                3 => ip_lookup(),
                4 => reverse_ip_lookup(),
                5 => break,
                _ => println!("Invalid choice!")
            }
        }
    }
}