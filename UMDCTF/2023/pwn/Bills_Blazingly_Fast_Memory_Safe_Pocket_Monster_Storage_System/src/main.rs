use std::{
    fs::{self, File},
    io::{self, Seek, SeekFrom, Write},
    path::{Path, PathBuf},
    process,
};

mod state;
use state::{PcBox, PcState};

mod poke;
use poke::{PokeMonster, MAX_POKEMONSTER_SIZE};

use crate::poke::index_to_poke;

const NAME: &'static str = "Bill's Blazingly Fast Memory Safe Pocket Monster Storage System";
const BOX_DIR: &'static str = "./boxes/";
const DB_DIR: &'static str = "./db/";

enum Choice {
    CreateBox,
    DeleteBox,
    List,
    Deposit,
    Withdraw,
    Quit,
    Unknown,
}

impl From<u32> for Choice {
    fn from(value: u32) -> Self {
        return match value {
            1 => Self::CreateBox,
            2 => Self::DeleteBox,
            3 => Self::List,
            4 => Self::Deposit,
            5 => Self::Withdraw,
            6 => Self::Quit,
            _ => Self::Unknown,
        };
    }
}

fn box_path(name: &str) -> PathBuf {
    let mut path = PathBuf::from(BOX_DIR);
    path.push(name);
    path
}

fn create_box_file(name: &str) -> Result<File, std::io::Error> {
    let path = box_path(name);

    File::options()
        .read(true)
        .write(true)
        .create_new(true)
        .open(path)
}

fn get_box_file(name: &str) -> Result<File, std::io::Error> {
    let path = box_path(name);

    File::options().read(true).write(true).open(path)
}

fn init() -> PcState {
    fs::create_dir_all(BOX_DIR).expect(&format!("failed to create {BOX_DIR}"));
    fs::create_dir_all(DB_DIR).expect(&format!("failed to create {DB_DIR}"));

    let path = Path::new(DB_DIR).join("boxes.db");
    let db_file = File::options()
        .read(true)
        .write(true)
        .create(true)
        .open(&path)
        .expect(&format!("failed to open {}", path.display()));

    PcState::load(db_file)
}

fn read_string(prompt: &str) -> String {
    print!("{prompt}");
    io::stdout().flush().expect("failed to flush stdout");

    let mut buf = String::new();
    io::stdin()
        .read_line(&mut buf)
        .expect("failed to read from stdin");

    buf
}

fn prompt_command() -> Choice {
    println!("Commands:");
    println!(" (1) Create a box");
    println!(" (2) Delete a box");
    println!(" (3) List Pocket Monsters™");
    println!(" (4) Deposit a Pocket Monster™");
    println!(" (5) Withdraw a Pocket Monster™");
    println!(" (6) Quit");

    match read_string("> ").trim().parse::<u32>() {
        Ok(x) => x.into(),
        Err(_) => Choice::Unknown,
    }
}

fn create_box(state: &mut PcState) {
    let name = read_string("Box Name: ");
    let name = name.trim();

    match create_box_file(name) {
        Ok(_) => {
            println!("Created box \"{name}\"");
            state.boxes.push(PcBox {
                name: name.to_string(),
                filled: Vec::new(),
            });
        }
        Err(e) => println!("Failed to open box \"{name}\": {e}"),
    }
}

fn delete_box(state: &mut PcState) {
    let name = read_string("Box Name: ");
    let name = name.trim();

    if get_box_file(name).is_err() {
        println!("Invalid box!");
        return;
    };

    state.boxes.retain(|b| b.name != name);
    if let Err(e) = fs::remove_file(box_path(name)) {
        println!("Failed to remove box: {e}");
    }
}

fn list(state: &PcState) {
    println!("--------------------------");
    for b in &state.boxes {
        let Ok(mut file) = get_box_file(&b.name) else {
            continue;
        };

        println!("Box {}:", b.name);

        for &i in &b.filled {
            // convert index into file offset
            let offset = i * MAX_POKEMONSTER_SIZE;
            file.seek(SeekFrom::Start(offset))
                .expect("failed to seek box file");

            if let Ok(monster) = bincode::deserialize_from::<_, PokeMonster>(&file) {
                let species = index_to_poke(monster.number);
                println!("- {i}: ({}) {}", species, monster.nickname);
            }
        }
    }
    println!("--------------------------");
}

fn deposit(state: &mut PcState) {
    let box_name = read_string("Box Name: ");
    let box_name = box_name.trim();

    let Ok(mut file) = get_box_file(box_name) else {
        println!("Invalid box!");
        return;
    };

    let Ok(slot) = read_string("Slot: ").trim().parse::<u64>() else {
        println!("Invalid slot!");
        return;
    };
    let Some(offset) = slot.checked_mul(MAX_POKEMONSTER_SIZE) else {
        println!("Invalid slot!");
        return;
    };
    if file.seek(SeekFrom::Start(offset)).is_err() {
        println!("Invalid slot!");
        return;
    }

    // check if there is already a pokemon there
    for b in &state.boxes {
        if b.name == box_name {
            if b.filled.binary_search(&slot).is_ok() {
                println!("Slot already filled!");
                return;
            }
            break;
        }
    }

    let Ok(number) = read_string("Pocket Monster™ Number: ").trim().parse::<usize>() else {
        println!("Invalid number!");
        return;
    };
    let nickname = read_string("Pocket Monster™ Nickname: ").trim().to_string();

    let new_poke = PokeMonster { nickname, number };
    if bincode::serialized_size(&new_poke).unwrap() > MAX_POKEMONSTER_SIZE {
        println!("Too big!");
        return;
    }
    if let Err(e) = bincode::serialize_into(&file, &new_poke) {
        println!("Failed to write: {e}");
        return;
    }

    println!("Pocket Monster™ deposited!");
    for b in &mut state.boxes {
        if b.name == box_name {
            match b.filled.binary_search(&slot) {
                Ok(_) => unreachable!(),
                Err(i) => b.filled.insert(i, slot),
            }
            break;
        }
    }
}

fn withdraw(state: &mut PcState) {
    let box_name = read_string("Box Name: ");
    let box_name = box_name.trim();

    let Ok(mut file) = get_box_file(box_name) else {
        println!("Invalid box!");
        return;
    };

    let Ok(slot) = read_string("Slot: ").trim().parse::<u64>() else {
        println!("Invalid slot!");
        return;
    };
    let Some(offset) = slot.checked_mul(MAX_POKEMONSTER_SIZE) else {
        println!("Invalid slot!");
        return;
    };
    if file.seek(SeekFrom::Start(offset)).is_err() {
        println!("Invalid slot!");
        return;
    }

    // check if there is actually a pokemon there
    for b in &mut state.boxes {
        if b.name == box_name {
            if let Ok(i) = b.filled.binary_search(&slot) {
                b.filled.remove(i);
                println!("matter_manipulator.so: cannot open shared object file: No such file or directory");
                println!("Pocket Monster™ withdrawn!");
            } else {
                println!("No Pocket Monster™ in slot!")
            }
            break;
        }
    }
}

fn main() {
    let mut state = init();
    println!("Welcome to {NAME}!");

    loop {
        match prompt_command() {
            Choice::CreateBox => create_box(&mut state),
            Choice::DeleteBox => delete_box(&mut state),
            Choice::List => list(&state),
            Choice::Deposit => deposit(&mut state),
            Choice::Withdraw => withdraw(&mut state),
            Choice::Quit => {
                println!("Goodbye!");
                process::exit(0);
            }
            Choice::Unknown => println!("Unknown command!"),
        }

        state.save();
    }
}
