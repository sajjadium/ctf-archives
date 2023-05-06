use std::error::Error;
use std::fs;
use std::io::{Read, Write};

const MAX_DATA_SIZE: usize = 1024;
const DEFAULT_STRING: &str = "Hello, World!";

const DEFAULT_SECRET: usize = 0x0123456789abcdef;
const WIN_SECRET: usize = 0xdeadbeefcafebabe;

#[repr(C)]
#[derive(Debug)]
struct Node {
    data: [u8; MAX_DATA_SIZE],
    data_size: usize,
    max_data_size: usize,
    canary: usize,
    secret: usize,
    next: Option<Box<Node>>,
}

impl Node {
    fn new(data: &str, canary: usize) -> Result<Self, Box<dyn Error>> {
        let mut res = Self {
            data: [0; MAX_DATA_SIZE],
            data_size: 0,
            max_data_size: 0,
            canary,
            secret: DEFAULT_SECRET,
            next: None,
        };

        let data_chars = data.chars().collect::<Vec<_>>();
        // Check length ahead of time to avoid buffer overflows.
        if data_chars.len() > MAX_DATA_SIZE {
            return Err("Data too long to set".into());
        }

        let node_data_pointer: *mut u8 = res.data.as_mut_ptr();
        let data_pointer: *const u8 = data.as_bytes().as_ptr();

        res.data_size = data.len();
        res.max_data_size = MAX_DATA_SIZE;
        unsafe {
            // This is safe because we've already validated data length.
            std::ptr::copy_nonoverlapping(data_pointer, node_data_pointer, res.data_size);
        }

        Ok(res)
    }

    fn set_data(&mut self, data: &str) -> Result<(), Box<dyn Error>> {
        // Validate that passed string isn't too long to fit in this Node's
        // data array.
        if data.len() > self.max_data_size {
            return Err("Data too long to set".into());
        }

        let data_chars = data.chars().collect::<Vec<_>>();
        // This is safe because we've already validated that data_chars is short enough
        // to fit in the bounds of our array (<= max_data_size).
        unsafe {
            for i in 0..data_chars.len() {
                *self.data.get_unchecked_mut(i) = (*data_chars.get_unchecked(i)) as u8;
            }
        }

        Ok(())
    }

    fn append_node(&mut self, data: &str, canary: usize) -> Result<(), Box<dyn Error>> {
        // Create new node.
        let old_next = self.next.take();

        let mut new_next = Node::new(data, canary)?;

        // Fixup next references.
        new_next.next = old_next;
        self.next = Some(Box::new(new_next));

        Ok(())
    }

    fn print(&self) -> Result<(), Box<dyn Error>> {
        for i in 0..self.data_size {
            unsafe {
                let this_byte = *self.data.get_unchecked(i);
                std::io::stdout().write_all(&[this_byte])?;
            }
        }
        println!();

        Ok(())
    }
}

fn help() {
    println!("\n****** Welcome to my Very Safe™ Linked List! ******");
    println!("\nPlease selection an option below:\n");
    println!("1) Help");
    println!("2) Set node data");
    println!("3) Print node data");
    println!("4) Print all nodes data");
    println!("5) Append node");
    println!("6) Go to next node");
    println!("7) Exit");
    println!();
}

// Use a canary to prevent buffer overflows. This is generated at random using /dev/urandom.
//
// This is Rust so buffer overflows are impossible but better safe than sorry ;)
fn generate_canary() -> Result<usize, Box<dyn Error>> {
    let mut canary_bytes: [u8; 8] = Default::default();
    let mut random_file = fs::File::open("/dev/urandom")?;
    random_file.read_exact(&mut canary_bytes)?;

    Ok(usize::from_be_bytes(canary_bytes))
}

fn set_node_data(node: &mut Node) -> Result<(), Box<dyn Error>> {
    print!("Data to set: ");
    std::io::stdout().flush()?; // blegh
    let mut data = String::new();
    std::io::stdin().read_line(&mut data)?;
    node.set_data(data.trim())
}

fn print_node_data(node: &Node) -> Result<(), Box<dyn Error>> {
    node.print()
}

fn print_all_nodes_data(node: &Node) -> Result<(), Box<dyn Error>> {
    let mut maybe_cur = Some(node);
    while let Some(cur) = maybe_cur {
        cur.print()?;
        maybe_cur = cur.next.as_deref();
        if maybe_cur.is_some() {
            println!("|\nv");
        }
    }
    println!("|\nv\nNULL");
    Ok(())
}

fn append_node(node: &mut Node, canary: usize) -> Result<(), Box<dyn Error>> {
    print!("New node data: ");
    std::io::stdout().flush()?;
    let mut data = String::new();
    std::io::stdin().read_line(&mut data)?;

    let mut end = node;
    while end.next.is_some() {
        end = end.next.as_mut().unwrap();
    }

    end.append_node(data.trim(), canary)
}

fn main() -> Result<(), Box<dyn Error>> {
    // Keep track of a canary to see if any funny business is occuring.
    let canary = generate_canary()?;

    let mut node = Box::new(Node::new(DEFAULT_STRING, canary)?);

    let mut input_text = String::new();

    help();

    loop {
        print!("\nPlease make your selection: ");
        std::io::stdout().flush()?;
        std::io::stdin().read_line(&mut input_text)?;

        let choice = input_text.trim().parse::<u32>()?;

        println!();
        match choice {
            1 => help(),
            2 => set_node_data(&mut node)?,
            3 => print_node_data(&node)?,
            4 => print_all_nodes_data(&node)?,
            5 => append_node(&mut node, canary)?,
            6 => node = node.next.ok_or("No more nodes to traverse!")?,
            7 => break,
            _ => return Err("invalid choice!".into()),
        };

        if node.canary != canary {
            println!("Hey! How'd you do that? That's not allowed :(");
            return Err("*** stack smashing detected ***".into());
        }

        input_text.clear();

        if node.secret == WIN_SECRET {
            println!("No way! Your brain is enormous!");
            let flag = fs::read_to_string("./flag")?;
            println!("Here's your flag: {}", flag);
            break;
        }
    }

    Ok(())
}
