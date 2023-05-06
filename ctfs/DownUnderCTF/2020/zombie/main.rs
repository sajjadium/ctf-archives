use std::{
	fs::read_to_string,
	io::{stdin, BufRead},
};

// Issue 25860

fn cell<'a, 'b, T: ?Sized>(_: &'a &'b (), v: &'b mut T) -> &'a mut T { v }

fn virus<'a, T: ?Sized>(input: &'a mut T) -> &'static mut T {
	let f: fn(_, &'a mut T) -> &'static mut T = cell;
	f(&&(), input)
}

fn zombie(size: usize) -> &'static mut [u8] {
	let mut object = vec![b'A'; size];
	let r = virus(object.as_mut());
	r
}

fn infect(lines: &mut impl Iterator<Item = std::io::Result<String>>) -> &'static mut [u8] {
	println!("How many people will you infect?");

	let line = lines.next().unwrap().unwrap();
	let size = line.parse::<usize>().unwrap();

	zombie(size)
}

fn eat_brains(
	lines: &mut impl Iterator<Item = std::io::Result<String>>,
	zombies: &mut Option<&mut [u8]>,
) {
	let r = match zombies {
		Some(r) => r,
		None => {
			println!("There are no zombies yet");
			return;
		}
	};

	loop {
		println!("Choose a victim.");
		let line = lines.next().unwrap().unwrap();
		if line.as_str() == "done" {
			break;
		}
		let index = line.parse::<usize>().unwrap();

		println!("Munch!");
		let line = lines.next().unwrap().unwrap();
		if line.as_str() == "done" {
			break;
		}
		let value = line.parse::<u8>().unwrap();
		r[index] = value;
	}
}

fn inspect_brains(
	lines: &mut impl Iterator<Item = std::io::Result<String>>,
	zombies: &mut Option<&mut [u8]>,
) {
	let r = match zombies {
		Some(r) => r,
		None => {
			println!("There are no zombies yet");
			return;
		}
	};

	loop {
		println!("Choose a brain.");
		let line = lines.next().unwrap().unwrap();
		if line.as_str() == "done" {
			break;
		}
		let index = line.parse::<usize>().unwrap();

		let thought = r[index];
		println!("Zombie {} is thinking: {}", index, thought);
	}
}

fn main() {
	let stdin = stdin();
	let mut lines = stdin.lock().lines();

	let mut infected = None;

	loop {
		println!("What will you do?");

		let line = lines.next().unwrap().unwrap();

		match line.as_str().trim() {
			"get flag" => continue,
			"infect" => infected = Some(infect(&mut lines)),
			"eat brains" => eat_brains(&mut lines, &mut infected),
			"inspect brains" => inspect_brains(&mut lines, &mut infected),
			_ => (),
		}

		if line.as_str().trim() == "get flag" {
			let flag = read_to_string("flag.txt").unwrap();
			println!("Here's the flag: {}", &flag);
		}
	}
}
