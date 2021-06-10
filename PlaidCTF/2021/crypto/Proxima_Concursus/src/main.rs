mod connect4;
mod digester;
mod secret;
mod stories;
mod utils;

use std::collections::HashMap;

use connect4::Connect4;
use digester::Digest;
use utils::{read, read_line, OrExitWith};

fn main() {
    println!("{}", stories::INTRO);

    loop {
        println!("{}", stories::CHOICE);

        let choice = read("Choice [0123]: ");
        println!();

        match choice {
            0 => observe(),
            1 => the_game(),
            2 => particle_collider(),
            3 => {
                println!("{}", stories::GOODBYE);
                std::process::exit(0)
            }
            _ => stories::desync(),
        }

        println!();
    }
}

fn observe() {
    println!("{}", stories::observe::INTRO);

    let x = hex::decode(read_line("Hex-encoded input: ")).or_exit_with("Not a valid hex string");
    println!("{}{}", stories::observe::RESULT, Digest::hex_digest_of(&x));
}

fn the_game() {
    println!("{}", stories::the_game::INTRO);
    let game_1 = read_line("Game 1 Log: ");

    if Connect4::play_game(&game_1).or_exit_with("Invalid Connect 4 game") != true {
        return Err("You were playing as 'x' and 'o' won").or_exit_with("Lost the Connect 4 game");
    }

    let game_2 = read_line("Game 2 Log: ");

    if Connect4::play_game(&game_2).or_exit_with("Invalid connect 4 game") != false {
        return Err("You were playing as 'o' and 'x' won").or_exit_with("Lost the Connect 4 game");
    }

    if Digest::hex_digest_of(game_1) == Digest::hex_digest_of(game_2) {
        secret::the_game::success();
    } else {
        return stories::desync();
    }
}

fn particle_collider() {
    const NEW_PARTICLE: &str = "inflaton";
    const POTENTIAL_PARTICLES: [&str; 14] = [
        "upquark",
        "downquark",
        "charmquark",
        "strangequark",
        "topquark",
        "bottomquark",
        "electron",
        "muon",
        "tau",
        "neutrino",
        "Zboson",
        "Wboson",
        "higgsboson",
        NEW_PARTICLE,
    ];

    println!("{}", stories::particle_collider::INTRO);

    let experimental_data: HashMap<String, String> = (0..4)
        .filter_map(|i| {
            let inp = hex::decode(read_line(format!(
                "Tuning parameters for particle {}: ",
                i + 1
            )))
            .or_exit_with("Invalid data");
            let dat = String::from_utf8_lossy(&inp);
            POTENTIAL_PARTICLES
                .iter()
                .filter(|&p| dat.starts_with(p))
                .next()
                .and_then(|p| Some((p.to_string(), Digest::hex_digest_of(inp))))
        })
        .collect();

    if !experimental_data.contains_key(NEW_PARTICLE) {
        return stories::desync();
    }

    if experimental_data.len() < 4 {
        return stories::desync();
    }

    println!("{}", stories::particle_collider::EXPERIMENT_SETUP);

    for e in experimental_data.values() {
        if e != &experimental_data[NEW_PARTICLE] {
            return stories::desync();
        }
    }

    secret::particle_collider::success();
}
