use futures::prelude::*;
use irc::client::prelude::*;
use log::{error, info, LevelFilter};
use rand::rngs::SmallRng;
use rand::{Rng, SeedableRng};
use simple_logger::SimpleLogger;
use std::fs;
use std::time::{SystemTime, UNIX_EPOCH};
use std::collections::HashMap;

fn get_roll() -> i32 {
    let seed = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    let mut rng = SmallRng::seed_from_u64(seed);
    rng.gen_range(1..101)
}

struct UserState {
    roll_to_beat: i32,
    wins: i32,
}

struct Bot {
    flag: String,
    state: HashMap<String, UserState>,
    client: Client,
}

impl Bot {
    async fn run(&mut self) -> irc::error::Result<()> {
        self.client.identify()?;
        let mut stream = self.client.stream()?;
        while let Some(message) = stream.next().await.transpose()? {
            match &message.command {
                Command::QUIT(_) => continue,
                Command::PRIVMSG(_, msg) => {
                    info!("{:?} {:?}", message.prefix, message.command);

                    let Some(target) = message.response_target() else {
                        info!("Failed to find target for message: {:#?}", message);
                        continue;
                    };

                    if msg.starts_with("!roll") {
                        self.handle_roll(target)?;
                    } else if msg.starts_with("!start") {
                        self.handle_start(target)?;
                    } else if msg.starts_with("!help") {
                        self.client.send_privmsg(
                            target,
                            "Use !start to start a game, and !roll to roll!",
                        )?;
                    }
                }
                _ => info!("{:?} {:?}", message.prefix, message.command),
            }
        }
        Ok(())
    }

    fn roll_self_for(state: &mut UserState) -> i32 {
        let mut roll = get_roll();
        if roll == 100 {
            roll = 1; // :)
        }
        state.roll_to_beat = roll;
        roll
    }

    fn handle_start(&mut self, target: &str) -> irc::error::Result<()> {
        if self.state.contains_key(target) {
            self.client
                .send_privmsg(target, "You're already in a game!")?;
        } else {
            let mut state = UserState {
                roll_to_beat: 0,
                wins: 0,
            };
            let roll = Bot::roll_self_for(&mut state);
            self.state.insert(target.to_string(), state);
            self.client.send_privmsg(
                target,
                format!("I rolled a {}. Good luck! Use !roll to roll.", roll),
            )?;
        }
        Ok(())
    }

    fn handle_roll(&mut self, target: &str) -> irc::error::Result<()> {
        let roll = get_roll();
        info!("{} rolled a {}", target, roll);
        self.client
            .send_privmsg(target, format!("{} rolls {} points", target, roll))?;

        let Some(mut state) = self.state.get_mut(target) else {
            self.client.send_privmsg(
                target,
                "Looks like you're not in a game yet. Use !start to start one!",
            )?;
            return Ok(());
        };

        if roll == state.roll_to_beat + 1 {
            self.client
                .send_privmsg(target, "How did you do that??? So lucky...")?;
            state.wins += 1;

            if state.wins >= 5 {
                self.client.send_privmsg(
                    target,
                    format!("Impossible!!! I give up, here's the flag: {}", self.flag),
                )?;
            }

            let next_roll = Bot::roll_self_for(&mut state);
            self.client.send_privmsg(
                target,
                format!(
                    "Bet you can't do it again... I rolled a {}. Good luck! Use !roll to roll.",
                    next_roll
                ),
            )?;
        } else if roll > state.roll_to_beat {
            self.client
                .send_privmsg(target, "You beat me! But it happens...")?;
            self.state.remove(target);
        } else {
            self.client.send_privmsg(target, "You lost!")?;
            self.state.remove(target);
        }
        Ok(())
    }
}

#[tokio::main]
async fn main() -> irc::error::Result<()> {
    SimpleLogger::new()
        .with_level(LevelFilter::Info)
        .init()
        .unwrap();
    let flag = fs::read_to_string("flag.txt").expect("Unable to read flag file");
    let mut bot = Bot {
        flag,
        state: HashMap::new(),
        client: Client::new("config.toml").await?,
    };

    match bot.run().await {
        Ok(_) => info!("Bot exited successfully"),
        Err(e) => error!("Bot exited with error: {}", e),
    }

    Ok(())
}
