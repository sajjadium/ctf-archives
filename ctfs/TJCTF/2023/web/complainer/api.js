const { v4: uuid } = require('uuid');

const posts = {};
const users = {};
const usernameToUserId = {};
const userIdToSession = {};

function createPost(userId, body) {
    const id = uuid();

    body = body.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');

    posts[id] = {
        id,
        userId,
        body,
    };

    users[userId].posts.add(id);

    return id;
}

function createUser(username, password) {
    if (username in usernameToUserId)
        throw 'Username already exists.';

    const id = uuid();

    users[id] = {
        id,
        username,
        password,
        posts: new Set(),
    };

    usernameToUserId[username] = id;

    return id;
}

function login(username, password) {
    const sessionId = uuid();
    const userId = usernameToUserId[username];

    if (!userId || users[userId].password !== password)
        throw 'Invalid username or password.';

    userIdToSession[userId] = sessionId;

    return { userId, sessionId };
}

function getUser(userId) {
    return {
        username: users[userId].username,
        userId: users[userId].id,
        posts: [...users[userId].posts].map(postId => posts[postId])
    };
}

function verifySession(userId, sessionId) {
    return userIdToSession[userId] && userIdToSession[userId] === sessionId;
}

function deleteSession(userId) {
    delete userIdToSession[userId];
}

function getPost(postId) {
    return posts[postId];
}


module.exports = {
    createPost,
    createUser,
    login,
    verifySession,
    getUser,
    deleteSession,
    getPost
};
