use anyhow::Result;
use flate2::{
    read::{GzDecoder, GzEncoder},
    Compression,
};
use serde::{Deserialize, Serialize};
use std::{
    io::{BufRead, Read},
    ops::{Deref, DerefMut},
    path::{Path, PathBuf},
};

use crate::GB_KEYS;

pub enum ReplayMode {
    Playback { keys_log: KeysLog, current: usize },
    Record { keys_log: KeysLog, path: PathBuf },
}

#[derive(Debug, Serialize, Deserialize)]
pub struct KeysLog(Vec<[bool; GB_KEYS]>);

impl Deref for KeysLog {
    type Target = Vec<[bool; GB_KEYS]>;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for KeysLog {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl KeysLog {
    pub fn new() -> KeysLog {
        KeysLog(Vec::new())
    }

    pub fn save_to_file<P: AsRef<Path>>(&self, path: P) -> Result<()> {
        let serialized = bincode::serialize(self)?;

        let mut gz = GzEncoder::new(&*serialized, Compression::default());
        let mut compressed = Vec::new();
        gz.read_to_end(&mut compressed)?;

        std::fs::write(path, compressed)?;
        Ok(())
    }

    pub fn read_from_file<P: AsRef<Path>>(path: P) -> Result<Self> {
        let compressed = std::fs::read(path)?;

        let mut gz = GzDecoder::new(&*compressed);
        let mut serialized = Vec::new();
        gz.read_to_end(&mut serialized)?;

        Ok(bincode::deserialize(&serialized)?)
    }

    pub fn read_from_stdin() -> Result<Self> {
        let b64encoded = std::io::stdin().lock().lines().next().unwrap()?;
        let compressed = base64::decode(b64encoded)?;

        let mut gz = GzDecoder::new(&*compressed);
        let mut serialized = Vec::new();
        gz.read_to_end(&mut serialized)?;

        Ok(bincode::deserialize(&serialized)?)
    }
}
