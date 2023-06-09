use std::cmp;

use crate::game::board::{Board, Player};

use crate::game::analysis::evaluate::evaluate;


const MIN_SCORE: i64 = i64::MIN + 1;
const MAX_SCORE: i64 = i64::MAX;


fn alphabeta(board: &Board, depth: usize, mut alpha: i64, mut beta: i64, is_maximizing_player: bool) -> (Option<usize>, i64) {
    if depth == 0 {
        return (None, evaluate(board, Player::Bot));
    } else if board.is_tie() {
        return (None, 0);
    } else if board.is_any_connect_four() {
        if board.is_connect_four(Player::Bot) {
            return (None, MAX_SCORE);
        } else {
            return (None, MIN_SCORE);
        }
    }

    let legal_moves = board.get_legal_moves();
    
    let mut best_move = *legal_moves.first().unwrap();
    let mut score;

    if is_maximizing_player {
        score = MIN_SCORE;
        
        for mcol in legal_moves {
            let mut new_board = (*board).clone();
            new_board.drop_piece(mcol, Player::Bot).unwrap();

            let (_, tmp_score) = alphabeta(&new_board, depth - 1, alpha, beta, false);
            if tmp_score > score {
                score = tmp_score;
                best_move = mcol;
            }

            alpha = cmp::max(alpha, score);
            if alpha >= beta {
                break
            }
        }
        (Some(best_move), score) 
    } else {
        score = MAX_SCORE;

        for mcol in legal_moves {
            let mut new_board = (*board).clone();
            new_board.drop_piece(mcol, Player::User).unwrap();

            let (_, tmp_score) = alphabeta(&new_board, depth - 1, alpha, beta, true);
            if tmp_score < score {
                score = tmp_score;
                best_move = mcol;
            }
            
            beta = cmp::min(beta, score);
            if alpha >= beta {
                break;
            }
        }
        (Some(best_move), score)
    }
}


pub fn search(board: &Board, depth: usize, _current_player: Player) -> usize {
    let (best_move, _) = alphabeta(board, depth, MIN_SCORE, MAX_SCORE, true);
    best_move.unwrap()
}
