const crypto = require('crypto')

const DEFAULT_CSRF = 'becbd4d21da153e4a4e28f658193b97e01ee03c8';

const db = Object.create(null)
db.users = Object.create(null)
db.cookies = Object.create(null)

function createNewUser(username, password) {
  db.users[username] = Object.create(null)
  db.users[username].name = username // By default the name = username
  db.users[username].password = password
}
// Create admin user
createNewUser(process.env.ADMIN_USERNAME, process.env.ADMIN_PASSWORD);

function getCsrf(cookie) {
  if (!cookie || !db.cookies[cookie]) return DEFAULT_CSRF;
  return db.cookies[cookie].csrf;
}

module.exports = {
  db,
  getCsrf,
  createNewUser,
}