const { randStr } = require('../utils')

const db = require('better-sqlite3')('db/database.db')
db.exec('DROP TABLE IF EXISTS answer; CREATE TABLE answer (word TEXT);')

const word = randStr(16)
const query = db.prepare('INSERT INTO answer (word) VALUES (?)')
query.run(word)

module.exports = db;
