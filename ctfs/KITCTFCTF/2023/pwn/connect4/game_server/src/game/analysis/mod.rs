use crate::game::board::{Board, Player};

mod search;
use search::search;

mod evaluate;


pub struct Analysis { eval_depth: usize }

impl Analysis {
    pub fn new (eval_depth: usize) -> Analysis {
        Analysis { eval_depth: eval_depth }
    }

    pub fn best_move(&self, current_board: &Board, current_player: Player) -> usize {
        search(current_board, self.eval_depth, current_player)
    }
}
