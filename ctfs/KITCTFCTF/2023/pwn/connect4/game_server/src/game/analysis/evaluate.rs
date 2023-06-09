use std::cmp;

use crate::game::board::{Board, Player, Field};


pub const CONNECT_FOUR_SCORE: i64 = 100000;

const CENTER_COLUMN_BONUS_MULTIPLIER: i64 = 5;

const OPPONENT_ONE_OF_CONNECT_FOUR_PENALTY: i64 = 25;

const PLAYER_OCCUPIED_THREE_SCORE: i64 = 50;
const PLAYER_OCCUPIED_TWO_SCORE: i64 = 20;


fn evaluate_slice(slice: Vec<Field>, player_to_move: Player) -> i64 {
    let opponent = match player_to_move {
        Player::User => Player::Bot,
        _ => Player::User
    };

    let mut player_occupied_count = 0;
    let mut empty_count = 0;
    let mut opponent_occupied_count = 0;

    for f in slice {
        match f {
            Field::Occupied(p) if p == player_to_move => player_occupied_count += 1,
            Field::Occupied(p) if p == opponent => opponent_occupied_count += 1,
            Field::Empty => empty_count += 1,
            _ => (),
        }
    }

    let opponent_is_one_of_connect_four = opponent_occupied_count == 3 && empty_count == 1;

    let mut score: i64 = if player_occupied_count == 4 {
        CONNECT_FOUR_SCORE
    } else if player_occupied_count == 3 && empty_count == 1 {
        PLAYER_OCCUPIED_THREE_SCORE
    } else if player_occupied_count == 2 && empty_count == 2 {
        PLAYER_OCCUPIED_TWO_SCORE
    } else {
        0
    };

    if opponent_is_one_of_connect_four {
        score -= OPPONENT_ONE_OF_CONNECT_FOUR_PENALTY;
    }

    cmp::max(0, score)
}


pub fn evaluate(board: &Board, player_to_move: Player) -> i64 {
    let mut score: i64 = 0;

    // center column pieces get a bonus
    let center_column_player_field_count = (0..board.height()).map(|row| board.field(row, board.width() >> 1))
        .filter(|f| *f == Field::Occupied(player_to_move)).count();
    score += (center_column_player_field_count as i64) * CENTER_COLUMN_BONUS_MULTIPLIER;

    // horizontal
    for row in 0..board.height() {
        for sc in 0..board.width()-3 {
            let slice = (0..4).map(|i| board.field(row, sc + i)).collect::<Vec<Field>>();
            score += evaluate_slice(slice, player_to_move);
        }
    }
    
    // vertical
    for col in 0..board.width() {
        for sr in 0..board.height()-3 {
            let slice = (0..4).map(|i| board.field(sr + i, col)).collect::<Vec<Field>>();        
            score += evaluate_slice(slice, player_to_move);
        }
    }
    

    // positive diagonal
    for col in 0..board.width()-3 {
        for row in 0..board.height()-3 {
            let slice = (0..4).map(|i| board.field(row + i, col + i)).collect::<Vec<Field>>();
            score += evaluate_slice(slice, player_to_move);
        }
    }
    

    // negative diagonal
    for col in 0..board.width()-3{
        for row in 3..board.height() {
            let slice = (0..4).map(|i| board.field(row - i, col + i)).collect::<Vec<Field>>();
            score += evaluate_slice(slice, player_to_move);
        }
    }
    
    score    
}
