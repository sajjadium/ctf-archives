'use strict';

const EC = require('elliptic').ec;
const fs = require('fs');

const encryption = require('./encryption.js');
var ec = new EC('p256');


class User {
    constructor(name, password, e2e, key) {
        this.name = name;
        this.password = password;
        this.e2e = e2e;
        this.messages = [];
        this.hidden = true;

        // remove prefix because it's incorrectly parsed by BN.js
        if (key !== undefined && key.startsWith('0x')) {
            key = key.slice(2);
        }

        if (!e2e) {
            if (key === undefined) {
                this.key = ec.genKeyPair().getPrivate('hex');
            } else {
                this.key = ec.keyFromPrivate(key, 'hex').getPrivate('hex');
            }
        } else {
            this.key = ec.keyFromPublic(key, 'hex').getPublic('hex');
        }
    }

    get_public_key(enc) {
        if (this.e2e) {
            return ec.keyFromPublic(this.key, 'hex').getPublic(enc || 16);
        } else {
            return ec.keyFromPrivate(this.key, 'hex').getPublic(enc || 16);
        }
    }

    derive_secret(pubkey) {
        if (this.e2e) {
            throw `User.derive_secret() can't be called when end-to-end encryption is enabled`;
        }
        return ec.keyFromPrivate(this.key, 'hex').derive(pubkey);
    }

    get_message_list(start, end) {
        if (start === undefined) {
            start = 0;
        }
        if (end === undefined || end > this.messages.length) {
            end = this.messages.length;
        }
        var messages = [];
        for (let id = start; id < end; id++) {
            var message = this.get_message(id);
            messages.push(message);
        }
        return messages;
    }

    get_message(id) {
        if (id < 0 || id >= this.messages.length) {
            return null;
        }

        var message = this.messages[id];
        var message_copy = Object.assign({}, message);
        message.seen = true;

        message_copy['id'] = id;

        // decrypt message if the sender and the recipient both exist and e2e is
        // disabled
        var peer;
        if (message.from === this.name) {
            peer = get_user(message.to);
        } else {
            peer = get_user(message.from);
        }
        if (peer == null || this.e2e) {
            return message_copy;
        }

        var secret = this.derive_secret(peer.get_public_key());

        try {
            message_copy['text'] = encryption.decrypt(message['encrypted'], secret, message['iv']);
            delete message_copy['encrypted'];
            delete message_copy['iv'];
        } catch {
            // return the encrypted message if decryption failed
        }

        return message_copy;
    }

    send_message(to, text, iv) {
        var to_user = get_user(to);
        if (to_user == null) {
            throw `user ${to} doesn't exist`;
        }

        var encrypted;
        if (!this.e2e) {
            // ignore iv if end-to-end encryption is disabled
            var iv = Date.now();
            const pubkey = to_user.get_public_key();
            const secret = this.derive_secret(pubkey);
            encrypted = encryption.encrypt(text, secret, iv);
        } else {
            // text and iv should be hexencoded
            encrypted = text;
            if (iv === undefined) {
                throw `iv is required`;
            }
        }

        let message = {
            from: this.name,
            to: to_user.name,
            date: Date.now(),
            iv: iv,
            encrypted: encrypted,
            seen: false,
        };
        this.messages.push(message);
        to_user.messages.push(message);
        console.log(`[*] message sent from ${this.name} to ${to_user.name}: ${message.encrypted}`);

        //console.log(JSON.stringify(USERS));
    }
}

function add_user(username, password, key, e2e) {
    if (username in USERS) {
        throw `user already exists`;
    }

    USERS[username] = new User(username, password, key, e2e);
    console.log(`[*] user ${username} created`);
}

function update_settings(user, settings) {
    const keys = ['hidden', 'password'];

    keys.forEach(key => {
        if (key in settings) {
            user[key] = settings[key];
            console.log(`[*] update settings of user ${user.name}: ${key} = ${settings[key]}`);
        }
    });
}

function list_users() {
    var users = [];
    for (const [name, user] of Object.entries(USERS)) {
        if (!user.hidden) {
            users.push(name);
        }
    }
    return users;
}

function delete_user(user) {
    const username = user.name;
    delete USERS[username];
    console.log(`[*] user ${username} deleted`);
}

function get_user(name) {
    if (!(name in USERS)) {
        return null;
    }
    return USERS[name];
}

function load_db(path) {
    var users = {};

    if (fs.existsSync(path)) {
        const data = fs.readFileSync(path);
        const json = JSON.parse(data);
        for (const [name, user] of Object.entries(json)) {
            users[name] = new User(user.name, user.password, user.e2e, user.key);
            users[name].hidden = user.hidden;
            users[name].messages = user.messages;
        }
    }

    return users;
}

var USERS = load_db('db.json');


module.exports = {
    add_user,
    delete_user,
    get_user,
    list_users,
    update_settings,
};
