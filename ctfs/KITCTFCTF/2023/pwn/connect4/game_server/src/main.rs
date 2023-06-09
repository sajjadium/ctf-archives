use std::{
    net::{TcpListener, TcpStream},
    io::{prelude::*, BufReader}
};
use rand::Rng;

mod crypto;
use crypto::{mod_exp, XSRng, EncStreamClient};

mod game;
use game::{Game, GameResult};


const GAMESERVER_HOST: &str = "127.0.0.1";
const GAMESERVER_PORT: usize = 7777;

const WINS_NEEDED: usize = 3;

const FLAG: &str = "GPNCTF{fake_flag}";

const PROFANITY_BLACKLIST: [&str; 5] = ["matemate", "miomate", "miomategood", "matemategood", "clubmatebad"];

const G: u32 = 30143167;
const P: u32 = 186047531;


fn run_gameserver() {
    let bind_str = format!("{}:{}", GAMESERVER_HOST, GAMESERVER_PORT);
    // println!("Listening on {}", bind_str);
    let listener = TcpListener::bind(bind_str).unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        // println!("Handling connection from {}!", stream.peer_addr().unwrap());
        match handle_connection(stream) {
            Ok(_) => (),
            // Err(e) => println!("Error during connection handling: {}", e)
            Err(_) => ()
        };
    }
}

fn handle_connection(mut stream: TcpStream) -> Result<(), std::io::Error> {
    let mut buf_reader = BufReader::new(stream.try_clone()?);
    let welcome_msg = format!("==========CONNECT 4==========\nWin {} games to collect your reward!\n", WINS_NEEDED);

    stream.write_all(welcome_msg.as_bytes())?;
    stream.write_all(b"Name for the leaderboard: ")?;

    let mut player_name = String::new();
    buf_reader.read_line(&mut player_name)?;
    
    if !has_profanity(&player_name) {
        stream.write_all(b"Good luck!\n\n")?;
    } else {
        let tmp_name = player_name.clone();
        // TODO: think of some tmp name format and switch name
        stream.write_all(format!("Your name contains profanity and cannot be used. Switching to temporary name...Your temporary name will be {}\n", tmp_name).as_bytes())?;
    }

    stream.write_all(b"Establishing secure session!\n")?;

    match establish_session(stream.try_clone()?)? {
        Some(session_key) => handle_secure_game(session_key, stream),
        _ => Ok(())
    }
}

fn establish_session(mut stream: TcpStream) -> Result<Option<u128>, std::io::Error> {
    let mut buf_reader = BufReader::new(stream.try_clone()?);

    let mut rng = rand::thread_rng();
    let privkey: u32 = rng.gen();

    let pubkey: u32 = mod_exp(G, privkey, P);

    stream.write_all(format!("{}\n", pubkey).as_bytes())?;

    let mut client_pubkey_data = String::new();
    buf_reader.read_line(&mut client_pubkey_data)?;

    if let Ok(client_pubkey) = client_pubkey_data.trim().parse::<u32>() {
        let shared: u32 = mod_exp(client_pubkey, privkey, P);
        
        let mut key: u128 = 0;
        let mut seeded_rng = XSRng::from_seed(shared);
        
        for _ in 0..4 {
            let x = seeded_rng.next();
            key = (key << 32) | (x as u128);
        }

        Ok(Some(key))
    } else {
        Ok(None)
    }
}

fn handle_secure_game(session_key: u128, stream: TcpStream) -> Result<(), std::io::Error> {
    let mut client = EncStreamClient::new(session_key, stream);
    
    let mut i = 0;
    loop {
        client.write_all(format!("Round {}\n", i + 1).as_bytes())?;
        let result = play_new_game_against_computer(&mut client)?;
        match result {
            GameResult::Tie => { client.write_all(b"It's a tie!\n")?; return Ok(()) }
            GameResult::PlayerLost => { client.write_all(b"You lost!\n")?; return Ok(()) }
            GameResult::PlayerWon => client.write_all(b"You won!\n")?,
        };

        i += 1;
        if i == WINS_NEEDED {
            client.write_all(b"Take your reward!\n")?;
            client.write_all(FLAG.as_bytes())?;
            client.write_all(b"\n")?;
            break;
        }
        // TODO: implement scoreboard
    }

    Ok(())
}

fn has_profanity(name: &String) -> bool {
    PROFANITY_BLACKLIST.iter().map(|phrase| name.contains(phrase)).any(|x| x)
}

fn play_new_game_against_computer(client: &mut EncStreamClient) -> Result<GameResult, std::io::Error> {
    let mut game = Game::new();
    
    while !game.is_game_over() {
        client.write_all(format!("{}\n", game).as_bytes())?;
        
        handle_player_move(&mut game, client)?;

        if !game.is_game_over() {
            let bot_move = game.make_bot_move();
            client.write_all(format!("Bot played: {}\n", bot_move).as_bytes())?;
        }
    }

    client.write_all(format!("{}\n", game).as_bytes())?;
    return Ok(game.result());
}

fn handle_player_move(game: &mut Game, client: &mut EncStreamClient) -> Result<(), std::io::Error> {
    loop {
        if let Some(player_move_col) = get_player_move(game, client)? {
            match game.make_move(player_move_col) {
                Ok(_) => break,
                Err(e) => client.write_all(format!("{}\n", e).as_bytes())?
            }
        }
    }
    Ok(())
}

fn get_player_move(game: &Game, client: &mut EncStreamClient) -> Result<Option<usize>, std::io::Error> {
    client.write_all(b"Your turn. Column? (1-7) ")?; 

    let mut player_move_data = String::new();
    client.read_line(&mut player_move_data)?;
    
    if let Ok(col) = player_move_data.trim().parse::<usize>() {
        if game.is_move_column_in_range(col) {
            Ok(Some(col - 1))
        } else {
            client.write_all(b"Number not in valid range\n")?; 
            Ok(None)
        }
    } else {
        client.write_all(b"Not a number\n")?;
        Ok(None)
    }
}



fn main() {
    run_gameserver();
}
