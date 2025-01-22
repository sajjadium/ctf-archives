use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Usage: cli_tool <name>");
        return;
    }
    println!("Hello, \{}!", args[1]);
}
