'use strict';

const crypto = require("crypto");

module.exports = { decrypt, encrypt };

function big_int_to_buffer(n, size) {
    var s = BigInt(n).toString(16);
    while (s.length < size * 2) {
        s = '0' + s;
    }
    return Buffer.from(s, 'hex');
}

function kdf(secret) {
    const key = big_int_to_buffer(secret, 32);
    return crypto.createHash('sha256').update(key).digest();
}

function encrypt(text, secret, iv) {
    const key = kdf(secret);
    iv = big_int_to_buffer(iv, 16);
    const cipher = crypto.createCipheriv("aes-256-cbc", key, iv);
    return cipher.update(text, "utf-8", "hex") + cipher.final("hex");
}

function decrypt(encrypted, secret, iv) {
    const key = kdf(secret);
    iv = big_int_to_buffer(iv, 16);
    const cipher = crypto.createDecipheriv("aes-256-cbc", key, iv);
    return cipher.update(encrypted, "hex", "utf-8") + cipher.final("utf-8");
}

module.exports = { big_int_to_buffer, decrypt, encrypt };
