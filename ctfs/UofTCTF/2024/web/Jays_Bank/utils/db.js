const util = require("util");
const mysql = require("mysql");

class DB {
  constructor() {
    this.conn = mysql.createConnection({
      host: process.env.DB_HOST,
      user: process.env.MYSQL_USER,
      password: process.env.MYSQL_PASSWORD,
      database: process.env.MYSQL_DATABASE,
      stringifyObjects: true,
    });

    this.query = util.promisify(this.conn.query).bind(this.conn);
  }

  connect() {
    return this.conn.connect();
  }

  async userExists(username) {
    const rows = await this.query("SELECT * FROM users WHERE username = ?", [
      username,
    ]);
    return rows.length > 0;
  }

  async register(username, password, data) {
    const rows = await this.query(
      "INSERT INTO users (username, password, data) VALUES (?, ?, ?)",
      [username, password, data]
    );
    return rows;
  }

  async login(username, password) {
    const rows = await this.query(
      "SELECT * FROM users WHERE username = ? AND password = ?",
      [username, password]
    );
    return rows.length > 0 ? rows[0] : null;
  }

  async getData(username) {
    const rows = await this.query("SELECT data FROM users WHERE username = ?", [
      username,
    ]);
    return rows.length > 0 ? rows[0].data : null;
  }

  async updateData(username, data) {
    const rows = await this.query(
      "UPDATE users SET data = ? WHERE username = ?",
      [data, username]
    );
    return rows;
  }
  
  convert(o) {
    return `{${Object.entries(o).map(([k, v]) => 
      `"${k}": ${typeof v === "object" && v !== null ? convert(v) : `"${v}"`}`
    ).join(", ")}}`.toLowerCase();
  }
  
  async verifyPassword(username, password) {
    const rows = await this.query(
      "SELECT * FROM users WHERE username = ? AND password = ?",
      [username, password]
    );
    return rows.length > 0;
  }

  async changePassword(username, password) {
    const rows = await this.query(
      "UPDATE users SET password = ? WHERE username = ?",
      [password, username]
    );
    return rows;
  }
}

module.exports = DB;
