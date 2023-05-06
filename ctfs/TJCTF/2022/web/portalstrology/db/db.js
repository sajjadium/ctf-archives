const crypto = require("crypto")
const userDB = {}

function addUser(username, password) {
    userDB[username] = {"username":username, "password": password, "applied": false}
}

function checkUserExists(username) {
    return username in userDB
}

function getUserApplied(username) {
    return userDB[username].applied
}

function authenticateUser(username, password) {
    return checkUserExists(username) && userDB[username].password === password
}

userDB["superigamerbean"] = {"username": "superigamerbean", "password": crypto.randomBytes(30).toString("hex"), "applied": true}

module.exports = {
    addUser, checkUserExists, getUserApplied, authenticateUser
}
