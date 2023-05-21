fn main() {
    println!("Welcome to the rattlespike playground!");
    println!("Send your code, followed by an EOF line.");
    let stdin = std::io::stdin();
    let mut code = String::new();
    loop {
        let mut line = String::new();
        stdin.read_line(&mut line).unwrap();
        if line.trim() == "EOF" {
            break;
        }

        code.push_str(&line);
    }

    let _ = rattlespike::run(code, "playground.spl".to_owned());
}
