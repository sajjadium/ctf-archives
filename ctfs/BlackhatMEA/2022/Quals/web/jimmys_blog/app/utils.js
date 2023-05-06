const sqlite = require("better-sqlite3");
const path = require("path");
const crypto = require("crypto")
const fs = require("fs");

const db = new sqlite(":memory:");

db.exec(`
    DROP TABLE IF EXISTS users;

    CREATE TABLE IF NOT EXISTS users (
        id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        username   VARCHAR(255) NOT NULL UNIQUE,
        admin      INTEGER NOT NULL
    )
`);

register("jimmy_jammy", 1);

function register(username, admin = 0) {
    try {
        db.prepare("INSERT INTO users (username, admin) VALUES (?, ?)").run(username, admin);
    } catch {
        return { success: false, data: "Username already taken" }
    }
    const key_path = path.join(__dirname, "keys", username + ".key");
    const contents = crypto.randomBytes(1024);
    fs.writeFileSync(key_path, contents);
    return { success: true, data: key_path };
}

function login(username, key) {
    const user = db.prepare("SELECT * FROM users WHERE username = ?").get(username);
    if (!user) return { success: false, data: "User does not exist" };

    if (key.length !== 1024) return { success: false, data: "Invalid access key" };
    const key_path = path.join(__dirname, "keys", username + ".key");
    if (key.compare(fs.readFileSync(key_path)) !== 0) return { success: false, data: "Wrong access key" };
    return { success: true, data: user };
}

module.exports = { register, login };