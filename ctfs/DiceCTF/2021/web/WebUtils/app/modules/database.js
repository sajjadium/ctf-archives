const Database = require('better-sqlite3')
const db = new Database('db.sqlite3')

const init = () => {
  db.prepare(`CREATE TABLE IF NOT EXISTS data(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT,
        data TEXT,
        type TEXT
        );`).run();
}

init();

const statements = {
  getData: db.prepare(`SELECT data, type FROM data WHERE uid = ?;`),
  addData: db.prepare(`INSERT INTO data (uid, data, type) VALUES (?, ?, ?);`)
}

module.exports = {
  getData: ({ uid }) => {
    return statements.getData.get(uid);
  },
  addData: ({ uid, data, type }) => {
    statements.addData.run(uid, data, type);
  },
  generateUid: (length) => {
    const characters =
      'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const arr = [];
    for (let i = 0; i < length; i++) {
      arr.push(
        characters.charAt(Math.floor(Math.random() * characters.length))
      );
    }
    return arr.join('');
  }
}
