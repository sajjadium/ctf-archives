const Database = require('./db');
const db = new Database();
const crypto = require('crypto');

const error = (message, status) => {
  const e = new Error(message);
  e.status = status;
  return e;
};

const generateId = () => {
  return crypto.randomBytes(16).toString('base64url');
};

module.exports = async (fastify, options, done) => {
  fastify.post(
    '/pastes',
    {
      schema: {
        body: {
          type: 'object',
          properties: {
            content: { type: 'string' },
          },
          required: ['content'],
        },
      },
    },
    (req) => {
      const id = generateId();
      db.createPaste(id, req.body.content);
      return { id };
    }
  );

  fastify.post(
    '/pastes/:id/comments',
    {
      schema: {
        body: {
          type: 'object',
          properties: {
            author: { type: 'string' },
            content: { type: 'string' },
          },
          required: ['author', 'content'],
        },
      },
    },
    (req) => {
      const { author, content } = req.body;
      if (content.length > 200) throw error('Comment too long!', 400);
      const post = { author, content };
      db.createComment(req.params.id, post);
      return post;
    }
  );

  fastify.get('/pastes/:id', (req) => ({
    content: db.getPaste(req.params.id),
  }));

  fastify.get('/pastes/:id/comments', (req) => db.getComments(req.params.id));

  done();
};
