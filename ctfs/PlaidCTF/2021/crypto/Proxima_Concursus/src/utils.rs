use crate::stories::exit_with;
use std::fmt::Display;
use std::io::{BufRead, Write};
use std::str::FromStr;

pub fn read_line(prompt: impl Display) -> String {
    print!("{}", prompt);
    std::io::stdout().flush().unwrap();
    let stdin = std::io::stdin();
    let line = stdin
        .lock()
        .lines()
        .next()
        .expect("Unexpected EOF")
        .or_exit_with("Input failed");
    line.trim().to_owned()
}

pub fn read<T>(prompt: impl Display) -> T
where
    T: FromStr,
    <T as FromStr>::Err: std::fmt::Display,
{
    read_line(prompt).parse().or_exit_with("Invalid input")
}

pub trait OrExitWith {
    type T;
    fn or_exit_with<S: std::fmt::Display>(self, x: S) -> Self::T;
}

impl<T> OrExitWith for Option<T> {
    type T = T;
    fn or_exit_with<S: std::fmt::Display>(self, x: S) -> Self::T {
        match self {
            Some(x) => x,
            None => exit_with(x),
        }
    }
}

impl<T, U> OrExitWith for Result<T, U>
where
    U: std::fmt::Display,
{
    type T = T;
    fn or_exit_with<S: std::fmt::Display>(self, x: S) -> Self::T {
        match self {
            Ok(x) => x,
            Err(e) => exit_with(format!("{}: {}", x, e)),
        }
    }
}
