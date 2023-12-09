const crypto = require('crypto');

const sha256 = plain => crypto.createHash('sha256').update(plain.toString()).digest('hex');
const random_bytes = size => crypto.randomBytes(size).toString();

module.exports = {
    sha256,
    random_bytes
}