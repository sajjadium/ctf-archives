#![feature(alloc_system)]

#![allow(while_true)]

extern crate alloc_system;

use std::collections::VecDeque;
use std::io;
use std::process;
use std::io::Write;

fn menu() {
    println!("1. Create a list");
    println!("2. Delete a list");
    println!("3. Edit a list");
    println!("4. Prepend to list");
    println!("5. Append to list");
    println!("6. View an element");
    println!("7. Exit");
}

fn create(lists: &mut Vec<VecDeque<i64>>) {
    println!("How big should this list be?");
    let mut list_size = String::new();
    prompt();
    io::stdin()
        .read_line(&mut list_size)
        .expect("failed to read input.");
    let list_size: usize = list_size.trim().parse().expect("invalid input");

    let new_vecdeque = VecDeque::with_capacity(list_size);

    lists.push(new_vecdeque);

    println!("Done!");
}

fn delete(lists: &mut Vec<VecDeque<i64>>) {
    println!("Which list do you want to delete?");
    let mut list_i = String::new();
    prompt();
    io::stdin()
        .read_line(&mut list_i)
        .expect("failed to read input.");
    let list_i: usize = list_i.trim().parse().expect("invalid input");

    lists.remove(list_i);

    println!("Done!");
}

fn edit(lists: &mut Vec<VecDeque<i64>>) {
    println!("Which list do you want to edit?");
    let mut list_i = String::new();
    prompt();
    io::stdin()
        .read_line(&mut list_i)
        .expect("failed to read input.");
    let list_i: usize = list_i.trim().parse().expect("invalid input");

    let vec_deque: &mut VecDeque<i64> = lists.get_mut(list_i).unwrap();

    println!("Okay, which element do you want to edit?");
    let mut list_i = String::new();
    prompt();
    io::stdin()
        .read_line(&mut list_i)
        .expect("failed to read input.");
    let list_i: usize = list_i.trim().parse().expect("invalid input");

    let element = vec_deque.get_mut(list_i).unwrap();
    
    println!("What do you want to set it to?");
    let mut new_val = String::new();
    prompt();
    io::stdin()
        .read_line(&mut new_val)
        .expect("failed to read input.");
    let new_val: i64 = new_val.trim().parse().expect("invalid input");

    *element = new_val;
}

fn prepend(lists: &mut Vec<VecDeque<i64>>) {
    println!("Which list do you want to prepend to?");
    let mut list_i = String::new();
    prompt();
    io::stdin()
        .read_line(&mut list_i)
        .expect("failed to read input.");
    let list_i: usize = list_i.trim().parse().expect("invalid input");

    let vec_deque: &mut VecDeque<i64> = lists.get_mut(list_i).unwrap();

    println!("How many elements do you want to prepend?");
    let mut num_new = String::new();
    prompt();
    io::stdin()
        .read_line(&mut num_new)
        .expect("failed to read input.");
    let num_new: usize = num_new.trim().parse().expect("invalid input");

    vec_deque.reserve(num_new);

    let mut c = 0;
    while c < num_new {

        println!("What value should be inserted?");
        let mut new_el = String::new();
        prompt();
        io::stdin()
            .read_line(&mut new_el)
            .expect("failed to read input.");
        let new_el: i64 = new_el.trim().parse().expect("invalid input");

        vec_deque.push_front(new_el);

        c += 1;
    }
}

fn append(lists: &mut Vec<VecDeque<i64>>) {
    println!("Which list do you want to append to?");
    let mut list_i = String::new();
    prompt();
    io::stdin()
        .read_line(&mut list_i)
        .expect("failed to read input.");
    let list_i: usize = list_i.trim().parse().expect("invalid input");

    let vec_deque: &mut VecDeque<i64> = lists.get_mut(list_i).unwrap();

    println!("How many elements do you want to append?");
    let mut num_new = String::new();
    prompt();
    io::stdin()
        .read_line(&mut num_new)
        .expect("failed to read input.");
    let num_new: usize = num_new.trim().parse().expect("invalid input");

    vec_deque.reserve(num_new);

    let mut c = 0;
    while c < num_new {

        println!("What value should be inserted?");
        let mut new_el = String::new();
        prompt();
        io::stdin()
            .read_line(&mut new_el)
            .expect("failed to read input.");
        let new_el: i64 = new_el.trim().parse().expect("invalid input");

        vec_deque.push_back(new_el);

        c += 1;
    }
}

fn view(lists: &mut Vec<VecDeque<i64>>) {
    println!("Which list do you want to view?");
    let mut list_i = String::new();
    prompt();
    io::stdin()
        .read_line(&mut list_i)
        .expect("failed to read input.");
    let list_i: usize = list_i.trim().parse().expect("invalid input");

    let vec_deque: &mut VecDeque<i64> = lists.get_mut(list_i).unwrap();

    println!("Which element do you want to view?");
    let mut list_i = String::new();
    prompt();
    io::stdin()
        .read_line(&mut list_i)
        .expect("failed to read input.");
    let list_i: usize = list_i.trim().parse().expect("invalid input");

    let element = vec_deque.get_mut(list_i).unwrap();

    println!("Value: {}", element);
}

fn prompt() {
    print!("> ");
    io::stdout().flush().unwrap();
}

fn main() {
    let mut lists: Vec<VecDeque<i64>> = Vec::new();

    println!("Welcome to my rustic service, which lets you manipulate lists at will!");
    println!("Due to a recent attack on our systems, we have greatly hardened our security, and are now memory-safe.");
    while true {
        menu();
        prompt();
        let mut choice = String::new();
        io::stdin()
            .read_line(&mut choice)
            .expect("failed to read input.");
        let choice: i32 = choice.trim().parse().expect("invalid input");

        match choice {
            1 => create(&mut lists),
            2 => delete(&mut lists),
            3 => edit(&mut lists),
            4 => prepend(&mut lists),
            5 => append(&mut lists),
            6 => view(&mut lists),
            7 => {
                println!("Bye!");
                process::exit(0);
            },
            _ => println!("Invalid choice!"),
        }
    }
}