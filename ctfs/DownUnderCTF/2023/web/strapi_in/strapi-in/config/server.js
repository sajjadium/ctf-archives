const crypto = require('crypto')

module.exports = ({ env }) => ({
  host: env('HOST', '0.0.0.0'),
  port: env.int('PORT', 1337),
  app: {
    keys: [
      crypto.randomBytes(64).toString('base64'),
      crypto.randomBytes(64).toString('base64'),
      crypto.randomBytes(64).toString('base64'),
      crypto.randomBytes(64).toString('base64')
    ],
  },
  webhooks: {
    populateRelations: env.bool('WEBHOOKS_POPULATE_RELATIONS', false),
  },
});
