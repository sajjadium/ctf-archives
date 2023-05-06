const Database = require('./db');
const db = new Database();

// make admin user
const crypto = require('crypto');
db.register('admin', crypto.randomBytes(32).toString('hex'));
db.addNote('admin', {
  body: process.env.FLAG,
  tag: 'private',
});

const error = (message, status) => {
  const e = new Error(message);
  e.status = status;
  return e;
};

module.exports = async (fastify, options, done) => {
  fastify.addHook('onRequest', (req, rep, done) => {
    const signedUsername = req.cookies?.username;
    const cookie = fastify.unsignCookie(signedUsername ?? '');

    if (cookie.valid) {
      req.auth = {
        login: true,
        username: cookie.value,
      };
      return done();
    }

    req.auth = {
      login: false,
      username: '',
    };
    done();
  });

  fastify.post(
    '/notes',
    {
      schema: {
        body: {
          type: 'object',
          properties: {
            body: { type: 'string' },
            tag: { type: 'string' },
          },
          required: ['body', 'tag'],
        },
      },
    },
    (req) => {
      if (!req.auth.login) throw error('Not logged in!', 401);
      if (req.auth.username === 'admin')
        throw error('No admin notes please!', 400);
      db.addNote(req.auth.username, {
        body: req.body.body,
        tag: req.body.tag,
      });
      return {};
    }
  );

  fastify.get('/notes/:username', (req) => {
    const notes = db.getNotes(req.params.username);
    if (req.params.username === req.auth.username) return notes;
    if (req.auth.username === 'admin') return notes;
    return notes.filter((note) => note.tag === 'public');
  });

  fastify.post(
    '/register',
    {
      schema: {
        body: {
          type: 'object',
          properties: {
            username: { type: 'string' },
            password: { type: 'string' },
          },
          required: ['username', 'password'],
        },
      },
    },
    (req, rep) => {
      if (db.getPassword(req.body.username) !== undefined)
        throw error('User already exists!', 403);
      db.register(req.body.username, req.body.password);
      rep.cookie('username', req.body.username, {
        expires: new Date().setFullYear(6969),
        path: '/',
        signed: true,
      });
      return {};
    }
  );

  fastify.post(
    '/login',
    {
      schema: {
        body: {
          type: 'object',
          properties: {
            username: { type: 'string' },
            password: { type: 'string' },
          },
          required: ['username', 'password'],
        },
      },
    },
    (req, rep) => {
      if (db.getPassword(req.body.username) === req.body.password) {
        rep.cookie('username', req.body.username, {
          expires: new Date().setFullYear(6969),
          path: '/',
          signed: true,
        });
        return {};
      }
      throw error('Incorrect username or password!', 401);
    }
  );

  fastify.get('/auth', (req) => req.auth);

  done();
};
