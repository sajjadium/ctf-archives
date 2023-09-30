use std::io::{self, Read, BufRead};

fn main() {
    let input = loop {
        match get_line() {
            Ok(my_str) => break my_str,
            Err(_) => {
                print!("Try again.");
                continue;
            }
        }
    };


    let mut output = String::new();

    for word in input.split_whitespace() {
        let first = &word[0..1];
        let rest = &word[1..];

        output += rest;
        output += first;
        output += "ay";
        output += " ";
    }

    print!("{output}");
}

fn get_line() -> Result<String, io::Error> {
    let mut input = String::new();

    io::BufReader::new(io::stdin().take(1862)).read_line(&mut input)?;

    Ok(input)
}
