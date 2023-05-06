use dashmap::DashMap;
use once_cell::sync::Lazy;
use rand::distributions::Alphanumeric;
use rand::{thread_rng, Rng};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

pub fn randstr(n: usize) -> String {
    thread_rng()
        .sample_iter(Alphanumeric)
        .take(n)
        .map(char::from)
        .collect()
}

// this is dumb but i am lazy :)
pub static DB: Lazy<DashMap<String, User>> = Lazy::new(DashMap::new);
pub static SESSIONS: Lazy<DashMap<String, String>> = Lazy::new(DashMap::new);

#[derive(Serialize)]
#[serde(rename_all = "lowercase")]
pub enum APIStatus {
    Success,
    Error,
}

#[derive(Serialize)]
pub struct APIResponse {
    pub status: APIStatus,
    pub data: Option<serde_json::Value>,
    pub message: Option<String>,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ShopItem {
    pub name: &'static str,
    pub image: &'static str,
    pub price: i32,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct PurchasedItem {
    pub name: String,
    pub quantity: i32,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct User {
    pub username: String,
    pub password: String,
    #[serde(default)]
    pub items: Vec<PurchasedItem>,
    #[serde(default = "default_money")]
    pub money: i32,
}

fn default_money() -> i32 {
    1000
}

pub fn sha256(input: String) -> String {
    format!("{:x}", Sha256::digest(input))
}

pub fn validate_body(body: &serde_json::Value, allowed: &[&str]) -> bool {
    if let Some(body) = body.as_object() {
        if body.keys().any(|key| !allowed.contains(&key.as_str())) {
            return false;
        }
    }
    true
}
