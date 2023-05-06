const argon2 = require('argon2');

const db = new Map();

const getUser = (username) => db.get("user_" + username);
const setUser = (username, user) => db.set("user_" + username, user); 
const hasUser = (username) => db.has("user_" + username);

const addUser = async (username, password) => {
    setUser(username, {
        password: await argon2.hash(password),
        notes: [],
        voiceMemo: null
    });
};

const checkLogin = async (username, password) => {
    if(!hasUser(username)) return false;
    let user = getUser(username);
    if(await argon2.verify(user.password, password)) return true;
    return false;
};

const addNote = (username, note) => getUser(username).notes.push(note);
const getNotes = (username) => getUser(username).notes;
const removeNote = (username, idx) => getUser(username).notes.splice(idx, 1);

const setMemo = (username, memo) => (getUser(username).voiceMemo = memo);
const getMemo = (username) => getUser(username).voiceMemo;

(async () => {
    if(!hasUser("admin")) {
        let password = require("crypto").randomBytes(16).toString("hex");
        await addUser("admin", password);
        setMemo("admin", "uploads/flag.mp3");
        console.log(`created admin user with password: ${password}`);
    }
})();

module.exports = {
    db,
    hasUser, addUser,
    checkLogin,
    addNote, getNotes, removeNote,
    setMemo, getMemo
};