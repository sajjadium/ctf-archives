const users = new Map();

const getUser = (name) => users.get(name);
const setUser = (name, data) => users.set(name, data);

(() => {
    const crypto = require("crypto");
    const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');

    const username = `admin-` + (process.env.ADMIN_SUFFIX || crypto.randomBytes(8).toString("hex"));
    const password = process.env.ADMIN_PASSWORD || crypto.randomBytes(16).toString("hex");
    setUser(username, Object.freeze({
        username,
        password: sha256(password),
        money: 133742069,
        isAdmin: true,
        contacts: Object.freeze([])
    }));
    console.log(`created account: ${username} with password ${password}`);
})();

module.exports = {
    getUser,
    setUser
};