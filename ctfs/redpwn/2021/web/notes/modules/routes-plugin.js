const path = require('path');

module.exports = async (fastify, options, done) => {
  fastify.get('/view/:username', (res, rep) => {
    return rep.sendFile('static/view.html', path.resolve(__dirname, '..'));
  });

  done();
};
