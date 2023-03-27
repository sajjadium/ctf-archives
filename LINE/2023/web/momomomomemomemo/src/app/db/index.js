import sqlite3 from 'sqlite3'
import crypto from 'crypto'

const db = await new sqlite3.Database('./data/db.sqlite3', (err) => {
    if (err) {
        console.error(err)
    } else {
        db.serialize(() => {
            db.run('CREATE TABLE IF NOT EXISTS user( \
                id TEXT PRIMARY KEY, \
                username TEXT UNIQUE, \
                password TEXT, \
                isadmin BOOLEAN \
            )')
            db.run('CREATE TABLE IF NOT EXISTS memo( \
                id TEXT PRIMARY KEY, \
                ownerId TEXT, \
                content TEXT \
            )')
            db.run('CREATE TABLE IF NOT EXISTS captcha_code( \
                userid TEXT PRIMARY KEY, \
                code TEXT \
            )')
            const adminId = crypto.randomUUID()
            db.run('INSERT OR IGNORE INTO user (id, username, password, isadmin) VALUES (?,?,?,true)', adminId, 'admin', process.env.ADMIN_PASSWORD || 'adminpassword')
            db.run('INSERT OR IGNORE INTO memo (id, ownerid, content) VALUES (?, ?, ?)', crypto.randomUUID(), adminId, process.env.FLAG)
        })
    }
})

const register = async(username, password) => {
    return new Promise((resolve, reject) => {
        db.run('INSERT INTO user (id, username, password, isadmin) VALUES (?, ?, ?, false)', crypto.randomUUID(), username, password, (err) => {
            if (err) {
                return reject(err)
            } else {
                return resolve()
            }
        })
    })
}

const getUserByUsername = async (username) => {
    return new Promise((resolve, reject) => {
        db.get('SELECT * FROM user WHERE username=?', username, (err, row) => {
            if (err) return reject(err)
            return resolve(row)
        })
    })
}

const addMemo = async (ownerId, content) => {
    return new Promise((resolve, reject) => {
        db.run('INSERT INTO memo (id, ownerId, content) VALUES (?, ?, ?)', crypto.randomUUID(), ownerId, content, (err) => {
            if (err) {
                return reject(err)
            } else {
                return resolve()
            }
        })
    })
}

const getOwnedMemos = async (ownerId) => {
    return new Promise((resolve, reject) => {
        db.all('SELECT * FROM memo WHERE ownerId=?', ownerId, (err, rows) => {
            if (err) return reject(err)
            return resolve(rows)
        })
    })
}

const getOwnedMemo = async (ownerId, memoId) => {
    return new Promise((resolve, reject) => {
        db.get('SELECT * FROM memo WHERE ownerId=? AND id=?', ownerId, memoId, (err, row) => {
            if (err) return reject(err)
            return resolve(row)
        })
    })
}

const getMemo = async (memoId) => {
    return new Promise((resolve, reject) => {
        db.get('SELECT * FROM memo WHERE id=?', memoId, (err, row) => {
            if (err) return reject(err)
            return resolve(row)
        })
    })
}

const setCaptchaCode = async (userId, code) => {
    return new Promise((resolve, reject) => {
        db.run('REPLACE INTO captcha_code (userid, code) VALUES (?, ?)', userId, code, (err)=> {
            if (err) return reject(err)
            return resolve()
        })
    })
}

const getCaptchaCode = async (userId) => {
    return new Promise((resolve, reject) => {
        db.get('SELECT * FROM captcha_code WHERE userid=?', userId, (err, row) => {
            if (err) return reject(err)
            return resolve(row)
        })
    })
}

export default {
    register,
    getUserByUsername,
    addMemo,
    getOwnedMemos,
    getOwnedMemo,
    getMemo,
    setCaptchaCode,
    getCaptchaCode
}