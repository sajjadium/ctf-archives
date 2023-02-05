#![forbid(unsafe_code)]

use anyhow::anyhow;
use serde::de::DeserializeOwned;
use serde_json::json;
use shakmaty::Position;

use crate::game::{ChessGame, Game};
use crate::{EngineMessage, EngineResponse, EngineState, STATE};

pub fn handle(msg: &EngineMessage) -> anyhow::Result<EngineResponse> {
    match msg.r#type.as_str() {
        "init" => init(msg),
        "get_state" => get_state(msg),
        "play_move" => play_move(msg),
        unk => Err(anyhow!("Unknown type '{unk}'")),
    }
}

fn get_data<T: DeserializeOwned>(data: &Option<serde_json::Value>) -> anyhow::Result<T> {
    let Some(data) = data else {
        return Err(anyhow!("Missing required data"));
    };
    Ok(serde_json::from_value(data.clone())?)
}

type InitData = String;
fn init(msg: &EngineMessage) -> anyhow::Result<EngineResponse> {
    let data: InitData = get_data(&msg.data).unwrap_or_default();

    if msg.id.len() > 16 || !msg.id.chars().all(char::is_alphanumeric) {
        return Ok(EngineResponse {
            new_type: Some("error".to_string()),
            data: Some(json!("Invalid game ID")),
        });
    }

    let mut state = STATE.lock().unwrap();

    if let Some(state) = state.get(&msg.id) {
        return Ok(EngineResponse {
            new_type: Some("error".to_string()),
            data: Some(json!(format!("The game '{:#?}' already exists", state))),
        });
    }

    let game = Game::start(&data);
    state.insert(msg.id.clone(), EngineState { game });

    Ok(EngineResponse {
        new_type: None,
        data: Some(json!("ready")),
    })
}

fn get_state(msg: &EngineMessage) -> anyhow::Result<EngineResponse> {
    match STATE.lock().unwrap().get(&msg.id) {
        Some(state) => Ok(EngineResponse {
            new_type: None,
            data: Some(json!({
                "current_fen": state.game.get_fen(),
                "moves": state.game.get_moves(),
                "history": state.game.moves.iter().map(|s| s.to_string()).collect::<Vec<String>>(),
                "turn": state.game.get_state().turn().to_string()
            })),
        }),
        None => Err(anyhow!("There is no game with id '{}'", msg.id)),
    }
}

type MoveData = String;
fn play_move(msg: &EngineMessage) -> anyhow::Result<EngineResponse> {
    let data: MoveData = get_data(&msg.data)?;
    match STATE.lock().unwrap().get_mut(&msg.id) {
        Some(state) => match state.game.make_move(&data) {
            Ok(_) => Ok(EngineResponse {
                new_type: None,
                data: None,
            }),
            Err(e) => Err(e),
        },
        None => Err(anyhow!("There is no game with id '{}'", msg.id)),
    }
}
