#![forbid(unsafe_code)]

use std::str::FromStr;

use anyhow::anyhow;
use shakmaty::{
    fen::{Epd, Fen},
    uci::Uci,
    CastlingMode, Chess, EnPassantMode, Move, Position,
};

#[derive(Debug)]
pub enum StartType {
    Fen,
    Epd,
}

// to store all moves and history
#[derive(Debug)]
pub struct Game<'a> {
    pub start_type: StartType,
    pub start: &'a str,
    pub moves: Vec<Move>,
}

static DEFAULT_FEN: &str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";

pub trait ChessGame {
    fn start(init: &str) -> Self;
    fn get_state(&self) -> Chess;
    fn get_fen(&self) -> String;
    fn get_moves(&self) -> Vec<String>;
    fn make_move(&mut self, m: &str) -> anyhow::Result<String>;
}

fn validate_fen<'a, 'b>(fen: &'b str, default: &'a &'b str) -> (StartType, &'a str) {
    match fen.parse::<Fen>() {
        Ok(_) => (StartType::Fen, fen),
        Err(_) => (StartType::Fen, default),
    }
}

fn validate_epd<'a, 'b>(epd: &'b str, default: &'a &'b str) -> (StartType, &'a str) {
    match epd.parse::<Epd>() {
        Ok(_) => (StartType::Epd, epd),
        Err(_) => (StartType::Fen, default),
    }
}

impl ChessGame for Game<'_> {
    fn start(init: &str) -> Self {
        let mut validator: fn(_, _) -> (StartType, &'static str) = validate_fen;
        if init.contains(';') {
            validator = validate_epd;
        }
        let data: (StartType, &str) = validator(init, &DEFAULT_FEN);
        Game {
            start_type: data.0,
            start: data.1,
            moves: Vec::new(),
        }
    }

    fn get_state(&self) -> shakmaty::Chess {
        let mut game: Chess = match self.start_type {
            StartType::Fen => self
                .start
                .parse::<Fen>()
                .unwrap()
                .into_position(CastlingMode::Standard)
                .unwrap(),
            StartType::Epd => self
                .start
                .parse::<Epd>()
                .unwrap()
                .into_position(CastlingMode::Standard)
                .unwrap(),
        };
        for m in &self.moves {
            game = game.play(m).unwrap();
        }
        game
    }

    fn get_fen(&self) -> String {
        Fen::from_position(self.get_state(), EnPassantMode::Legal).to_string()
    }

    fn get_moves(&self) -> Vec<String> {
        self.get_state()
            .legal_moves()
            .iter()
            .map(|s| s.to_uci(CastlingMode::Standard).to_string())
            .collect()
    }

    fn make_move(&mut self, m: &str) -> anyhow::Result<String> {
        let game = self.get_state();
        let uci = Uci::from_str(m)?;
        let legal_move = uci.to_move(&game)?;
        match game.play(&legal_move) {
            Ok(_) => {
                self.moves.push(legal_move);
                Ok(self.get_fen())
            }
            Err(_) => Err(anyhow!("Invalid move")),
        }
    }
}
