use std::fmt;


const BOARD_WIDTH: usize = 7;
const BOARD_HEIGHT: usize = 6;
const BOARD_SIZE: usize = BOARD_WIDTH * BOARD_HEIGHT;


#[derive(Debug, Copy, Clone, PartialEq)]
pub enum Player {
    User,
    Bot
}

impl fmt::Display for Player {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let player_str = match self {
            Player::User => 'P',
            Player::Bot => 'B'
        };

        write!(f, "{}", player_str)
    }
}


#[derive(Debug, Copy, Clone, PartialEq)]
pub enum Field {
    Occupied(Player),
    Empty
}

impl fmt::Display for Field {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Field::Occupied(player) => write!(f, "{}", player)?,
            Field::Empty => write!(f, " ")?
        };

        Ok(())
    }
}


#[derive(Clone)]
pub struct Board {
    board_data: [Field; BOARD_SIZE],
}

impl Board {
    pub fn new() -> Board {
        Board { board_data: [Field::Empty; BOARD_SIZE] }
    }

    pub fn field(&self, row: usize, col: usize) -> Field {
        self.board_data[row * self.width() + col]
    }

    fn field_is_occupied(&self, row: usize, col: usize) -> bool {
        self.field_is_occupied_by(row, col, Player::User) || self.field_is_occupied_by(row, col, Player::Bot)
    }

    fn field_is_occupied_by(&self, row: usize, col: usize, player: Player) -> bool {
        match self.field(row, col) {
            Field::Occupied(p) => p == player,
            Field::Empty => false
        }
    }

    pub fn first_free_row_in_column(&self, col: usize) -> Option<usize> {
        for row in (0..self.height()).rev() {
            if !self.field_is_occupied(row, col) {
                return Some(row)
            }
        }
        None
    }

    fn column_is_full(&self, col: usize) -> bool {
        self.first_free_row_in_column(col).map(|_| false).unwrap_or(true)
    }

    pub fn set_field(&mut self, row: usize, col: usize, field: Field) {
        let board_width = self.width();
        self.board_data[row * board_width + col] = field;
    }

    pub fn drop_piece(&mut self, col: usize, player: Player) -> Option<usize> {
        if let Some(row) = self.first_free_row_in_column(col) {
            self.set_field(row, col, Field::Occupied(player));
            Some(row)
        } else {
            None
        }
    }

    pub fn height(&self) -> usize {
        BOARD_HEIGHT
    }

    pub fn width(&self) -> usize {
        BOARD_WIDTH
    }

    pub fn is_connect_four(&self, player: Player) -> bool {
        // horizontal
        for row in 0..self.height() {
            for sc in 0..self.width()-3 {
                if (0..4).map(|i| self.field_is_occupied_by(row, sc + i, player)).all(|x| x) {
                    return true;
                }
            }

        }
        
        // vertical
        for col in 0..self.width() {
            for sr in 0..self.height()-3 {
                if (0..4).map(|i| self.field_is_occupied_by(sr + i, col, player)).all(|x| x) {
                    return true;
                }
            }

        }

        // positive diagonal
        for col in 0..self.width()-3 {
            for row in 0..self.height()-3 {
                if (0..4).map(|i| self.field_is_occupied_by(row + i, col + i, player)).all(|x| x) {
                    return true;
                }
            }
        }

        // negative diagonal
        for col in 0..self.width()-3{
            for row in 3..self.height() {
                if (0..4).map(|i| self.field_is_occupied_by(row - i, col + i, player)).all(|x| x) {
                    return true;
                }
            }
        }

        false
    }

    pub fn is_any_connect_four(&self) -> bool {
        self.is_connect_four(Player::User) || self.is_connect_four(Player::Bot)
    }

    pub fn get_legal_moves(&self) -> Vec<usize> {
        (0..self.width()).filter(|col| !self.column_is_full(*col)).collect()
    }

    pub fn is_tie(&self) -> bool {
        !self.is_any_connect_four() && (0..self.width()).map(|col| self.column_is_full(col)).all(|x| x)
    }

    pub fn is_move_column_in_range(&self, col: usize) -> bool {
        col >= 1 && col <= self.width()
    }

}

impl fmt::Display for Board {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        for row in 0..self.height() {
            for col in 0..self.width() {
                write!(f, "| {} |", self.field(row, col))?;
            }
            write!(f, "\n")?;
        }
        Ok(())
    }
}
