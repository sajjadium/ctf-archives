const crypto = require("crypto");

const sha256 = (data) => crypto.createHash("sha256").update(data).digest("hex");
const users = new Map();
const posts = new Map();

(() => {
    let flagId = crypto.randomUUID();
    console.log(`flag post ID: ${flagId}`);

    posts.set(flagId, {
        name: "Flag",
        body: process.env.FLAG || "flag{test_flag}"
    });

    users.set("admin", Object.freeze({
        user: "admin",
        pass: sha256(process.env.ADMIN_PASSWORD || "password"),
        posts: Object.freeze([flagId]),
        todos: Object.freeze([])
    }));

    console.log(`created user admin | ${process.env.ADMIN_PASSWORD || "password"}`)
})();

module.exports = { users, posts };