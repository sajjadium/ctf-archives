use std::fmt;

mod board;
use board::{Player, Board};

mod analysis;
use analysis::Analysis;


const EVAL_DEPTH: usize = 6;


#[derive(Debug, Clone, Copy, PartialEq)]
pub enum GameResult {
    PlayerWon,
    PlayerLost,
    Tie,
}

pub struct Game {
    board: Board,
    current_player: Player
}


impl Game {
    pub fn new() -> Game {
        Game { board: Board::new(), current_player: Player::User }
    }

    pub fn is_game_over(&self) -> bool {
        self.board.is_connect_four(self.current_player) || self.board.is_tie() 
    }

    pub fn make_move(&mut self, col: usize) -> Result<(), &str> {
        if self.board.drop_piece(col, self.current_player).is_some() {
            self.next_player();
            Ok(())
        } else {
            Err("Invalid move")
        }
    }

    pub fn make_bot_move(&mut self) -> usize {
        let analysis = Analysis::new(EVAL_DEPTH);
        let best_move = analysis.best_move(&self.board, Player::Bot);
        self.make_move(best_move).unwrap();
        best_move + 1        
    }

    fn next_player(&mut self) {
        if !self.is_game_over() {
            if self.current_player == Player::User {
                self.current_player = Player::Bot;
            } else {
                self.current_player = Player::User;
            }
        }
    }

    pub fn result(&self) -> GameResult {
        if self.board.is_connect_four(self.current_player) {
            match self.current_player {
                Player::User => GameResult::PlayerWon,
                Player::Bot => GameResult::PlayerLost
            }
        } else {
            GameResult::Tie
        }        
    }

    pub fn is_move_column_in_range(&self, col: usize) -> bool {
        self.board.is_move_column_in_range(col)
    }
}

impl fmt::Display for Game {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Current Player: {}\n{}\n", self.current_player, self.board)
    }
}
