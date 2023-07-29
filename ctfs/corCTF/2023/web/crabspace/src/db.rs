use dashmap::DashMap;
use once_cell::sync::Lazy;
use serde::Serialize;
use uuid::Uuid;

#[derive(Debug, Serialize, Clone)]
pub struct User {
    pub id: Uuid,
    pub name: String,
    pub pass: String,
    pub following: Vec<Uuid>,
    pub followers: Vec<Uuid>,
    pub space: String,
}

pub static USERS: Lazy<DashMap<Uuid, User>> = Lazy::new(DashMap::new);
pub static NAMES: Lazy<DashMap<String, Uuid>> = Lazy::new(DashMap::new);

pub fn reset() {
    USERS.clear();
    NAMES.clear();

    let flag = std::fs::read_to_string("/flag.txt")
        .unwrap_or_else(|_| "corctf{test_flag}".to_string())
        .trim()
        .to_string();
    let admin = Uuid::new_v4();
    println!("[!] Admin account: {admin}");

    USERS.insert(
        admin,
        User {
            id: admin,
            name: "admin".to_string(),
            pass: flag,
            following: vec![],
            followers: vec![],
            space: "Nothing to see here...".to_string(),
        },
    );
    NAMES.insert("admin".to_string(), admin);
}
