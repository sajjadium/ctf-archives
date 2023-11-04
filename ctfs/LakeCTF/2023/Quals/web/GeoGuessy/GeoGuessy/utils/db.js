const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./db.sqlite');


function registerUser(username, token) {
    return new Promise((resolve, reject) => {
        db.run("INSERT INTO users VALUES (?,?,0)", [username, token], (err) => {
            if (err) {
                reject(err);
            } else {
                resolve();
            }
        })
    })
}

function getUserBy(byWhat, value) {
    if (typeof value != "string") return null;
    return new Promise((resolve, reject) => {
        ["username","token"].includes(byWhat) || reject("Invalid byWhat");
        db.get(`SELECT * FROM users WHERE ${byWhat}=?`, [value], async (err, row) => {
            if (err) {
                reject(err);
            } else {
                resolve(row)
            }
        });
    });
};

async function addNotificationToUserToken(userToken, notification) {
    db.run("DELETE FROM notifications WHERE userToken = ? and id not in (select id from notifications WHERE userToken = ? order by id desc limit 4)", [userToken,userToken]) // ty https://stackoverflow.com/questions/6528117/keep-only-n-last-records-in-sqlite-database-sorted-by-date
    return new Promise((resolve, reject) => {
        db.run("INSERT INTO notifications(userToken, notificationText) VALUES (?,?)", [userToken, notification], (err) => {
            if (err) {
                reject(err);
            } else {
                app.emit('event:new_notification', userToken);
                resolve()
            }
        })
    })
};

async function getNotificationsFromToken(token) {
    return new Promise((resolve, reject) => {
        db.all(`SELECT notificationText FROM notifications WHERE userToken=?`, [token], async (err, row) => {
            if (err) {
                reject(err);
            } else {
                resolve(row)
            }
        });
    });
};

async function updateUserByToken(token, newData) {
    return new Promise((resolve, reject) => {
        db.get("UPDATE users SET username=?, isPremium=? WHERE token = ?", [newData.username, newData.isPremium, token], async (err) => {
            if (err) {
                reject(err);
            } else {
                resolve()
            }
        });
    });
};

async function createChallenge(id,author,longitude,latitude,image,OpenLayersVersion,winText) {
    return new Promise((resolve, reject) => {
        db.get("INSERT INTO challenges VALUES (?, ?, ?, ?, ?, ?, ?)", [id,author,longitude,latitude,image,OpenLayersVersion,winText], async (err) => {
            if (err) {
                reject(err);
            } else {
                resolve()
            }
        });
    });
};

async function getChallengeById(id) {
    return new Promise((resolve, reject) => {
        db.get(`SELECT * FROM challenges WHERE id=?`, [id], async (err, row) => {
            if (err) {
                reject(err);
            } else {
                resolve(row)
            }
        });
    });
}

async function init(app) {
    global.app = app;
    db.exec(`
    CREATE TABLE IF NOT EXISTS users (
        username text primary key not null unique,
        token text not null unique,
        isPremium integer
        )
    `)
    db.exec(`
    CREATE TABLE IF NOT EXISTS notifications (
        id integer primary key autoincrement,
        userToken text not null,
        notificationText text not null
        )
    `)
    db.exec(`
    CREATE TABLE IF NOT EXISTS challenges (
        id text not null unique,
        author text not null,
        longitude text not null,
        latitude text not null,
        image text not null,
        OpenLayersVersion text not null,
        winText text not null
        )
    `)
}

module.exports = {registerUser, getUserBy, addNotificationToUserToken, updateUserByToken, getNotificationsFromToken, getChallengeById, createChallenge, init }
