const path = require('path');

module.exports = async (fastify, options, done) => {
  fastify.get('/paste/:id', (res, rep) => {
    return rep.sendFile('static/paste.html', path.resolve(__dirname, '..'));
  });

  done();
};
