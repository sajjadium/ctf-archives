const crypto = require('crypto')

module.exports = ({ env }) => ({
  auth: {
    secret: crypto.randomBytes(64).toString('base64'),
  },
  apiToken: {
    salt: crypto.randomBytes(64).toString('base64'),
  },
  transfer: {
    token: {
      salt: crypto.randomBytes(64).toString('base64'),
    },
  },
});
