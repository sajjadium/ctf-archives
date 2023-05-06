use std::{
    fs::File,
    io::{Seek, SeekFrom},
};

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct PcBox {
    pub name: String,
    pub filled: Vec<u64>,
}

pub struct PcState {
    pub boxes: Vec<PcBox>,
    db_file: File,
}

impl PcState {
    pub fn load(mut db_file: File) -> Self {
        db_file
            .seek(SeekFrom::Start(0))
            .expect("failed to seek db file");
        match bincode::deserialize_from(&mut db_file) {
            Ok(boxes) => PcState { boxes, db_file },
            Err(_) => PcState {
                boxes: Vec::new(),
                db_file,
            },
        }
    }

    pub fn save(&mut self) {
        self.db_file
            .seek(SeekFrom::Start(0))
            .expect("failed to seek db file");
        bincode::serialize_into(&mut self.db_file, &self.boxes)
            .expect("failed to serialize into db file");
    }
}
