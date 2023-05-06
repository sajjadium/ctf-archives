#![forbid(unsafe_code)]

use once_cell::sync::Lazy;
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::collections::HashMap;
use std::sync::Mutex;
use wasm_bindgen::prelude::*;

mod game;
mod handler;

#[derive(Debug)]
pub struct EngineState<'a> {
    game: game::Game<'a>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EngineMessage {
    id: String,
    r#type: String,
    data: Option<serde_json::Value>,
}

pub struct EngineResponse {
    new_type: Option<String>,
    data: Option<serde_json::Value>,
}

pub static STATE: Lazy<Mutex<HashMap<String, EngineState>>> =
    Lazy::new(|| Mutex::new(HashMap::new()));

#[wasm_bindgen]
pub fn handle(input: String) -> JsValue {
    let serializer = serde_wasm_bindgen::Serializer::json_compatible();
    let input: Result<EngineMessage, serde_json::Error> = serde_json::from_str(&input);

    let Ok(input) = input else {
        return EngineMessage {
            id: "error".to_string(),
            r#type: "error".to_string(),
            data: Some(json!("Invalid input"))
        }.serialize(&serializer).unwrap();
    };

    match handler::handle(&input) {
        Ok(res) => EngineMessage {
            id: input.id,
            r#type: res.new_type.unwrap_or(input.r#type),
            data: res.data,
        },
        Err(e) => EngineMessage {
            id: input.id,
            r#type: "error".to_string(),
            data: Some(json!(e.to_string())),
        },
    }
    .serialize(&serializer)
    .unwrap()
}
