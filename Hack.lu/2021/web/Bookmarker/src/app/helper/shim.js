const crypto = require('crypto')

const {
    LINK_SHIM_SECRET,
} = process.env


const generateHash = (url, username) => {
    let hash = crypto.createHash('sha256').update(`${url}|${username}|${LINK_SHIM_SECRET}`)
    return hash.digest('hex')
}

module.exports = {
    generateHash
}