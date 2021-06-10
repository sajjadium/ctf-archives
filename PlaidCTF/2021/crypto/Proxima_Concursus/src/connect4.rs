use crate::stories;

#[derive(Clone, Copy, PartialEq, Eq, Debug)]
enum Position {
    Filled { first_player: bool },
    Empty,
}

impl Default for Position {
    fn default() -> Self {
        Position::Empty
    }
}

pub struct Connect4 {
    next_player_is_first: bool,
    state: [[Position; Self::HEIGHT]; Self::WIDTH],
    heights: [usize; Self::WIDTH],
    latest_move: usize,
}

impl Connect4 {
    const WIDTH: usize = 10;
    const HEIGHT: usize = 8;
    const CHECK_DIRECTIONS: [(isize, isize); 7] = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (1, -1),
        (1, 0),
        (1, -1),
    ];

    fn print_game_state(&self) {
        print!("+");
        for _ in 0..Self::WIDTH {
            print!("-+");
        }
        println!();
        for i in 0..Self::HEIGHT {
            print!("|");
            for j in 0..Self::WIDTH {
                print!(
                    "{}|",
                    match self.state[j][Self::HEIGHT - 1 - i] {
                        Position::Empty => ' ',
                        Position::Filled { first_player } =>
                            if first_player {
                                'x'
                            } else {
                                'o'
                            },
                    }
                );
            }
            println!();
        }
        print!("+");
        for _ in 0..Self::WIDTH {
            print!("-+");
        }
        println!();
    }

    fn winner(&self) -> Option<bool> {
        let latest_posn_i = self.latest_move;
        let latest_posn_j = {
            let h = self.heights[latest_posn_i];
            if h == 0 {
                // Game hasn't started yet
                return None;
            } else {
                h - 1
            }
        };
        let latest_player = self.state[latest_posn_i][latest_posn_j];
        let winner_is_first_player = match latest_player {
            Position::Filled { first_player } => first_player,
            Position::Empty => unreachable!(),
        };

        'dirn: for (diri, dirj) in &Self::CHECK_DIRECTIONS {
            for mult in 1..=3 {
                let pi = {
                    let v = latest_posn_i as isize + mult * diri;
                    if v < 0 || v >= Self::WIDTH as _ {
                        continue 'dirn;
                    }
                    v as usize
                };
                let pj = {
                    let v = latest_posn_j as isize + mult * dirj;
                    if v < 0 || v >= Self::HEIGHT as _ {
                        continue 'dirn;
                    }
                    v as usize
                };
                if self.state[pi][pj] != latest_player {
                    continue 'dirn;
                }
            }
            return Some(winner_is_first_player);
        }
        return None;
    }

    fn play(&mut self, position: usize) -> Result<(), String> {
        let height = self.heights.get_mut(position).ok_or("Invalid position")?;
        let hole = self.state[position]
            .get_mut(*height)
            .ok_or("Overfull position")?;
        assert_eq!(*hole, Position::Empty);

        *hole = Position::Filled {
            first_player: self.next_player_is_first,
        };
        self.next_player_is_first = !self.next_player_is_first;
        *height += 1;
        self.latest_move = position;

        Ok(())
    }

    pub fn play_game(s: &str) -> Result<bool, String> {
        if !s.bytes().all(|x| x >= b'0' && x <= b'9') {
            return Err("Invalid game log".into());
        }

        let moves: Vec<usize> = s.bytes().map(|x| x as usize - '0' as usize).collect();

        let mut game = Self {
            next_player_is_first: true,
            state: Default::default(),
            heights: Default::default(),
            latest_move: 0,
        };

        for mv in moves {
            if game.winner().is_some() {
                return Err("Game ended early".into());
            }
            game.print_game_state();
            stories::sleep();
            game.play(mv)?;
        }
        game.print_game_state();

        game.winner().ok_or("No game winner".into())
    }
}
