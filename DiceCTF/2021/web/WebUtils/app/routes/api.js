const database = require('../modules/database');

module.exports = async (fastify) => {
  fastify.post('createLink', {
    handler: (req, rep) => {
      const uid = database.generateUid(8);
      const regex = new RegExp('^https?://');
      if (! regex.test(req.body.data))
        return rep
          .code(200)
          .header('Content-Type', 'application/json; charset=utf-8')
          .send({
            statusCode: 200,
            error: 'Invalid URL'
          });
      database.addData({ type: 'link', ...req.body, uid });
      rep
        .code(200)
        .header('Content-Type', 'application/json; charset=utf-8')
        .send({
          statusCode: 200,
          data: uid
        });
    },
    schema: {
      body: {
        type: 'object',
        required: ['data'],
        properties: {
          data: { type: 'string' }
        }
      }
    }
  });

  fastify.post('createPaste', {
    handler: (req, rep) => {
      const uid = database.generateUid(8);
      database.addData({ type: 'paste', ...req.body, uid });
      rep
        .code(200)
        .header('Content-Type', 'application/json; charset=utf-8')
        .send({
          statusCode: 200,
          data: uid
        });
    },
    schema: {
      body: {
        type: 'object',
        required: ['data'],
        properties: {
          data: { type: 'string' }
        }
      }
    }
  });

  fastify.get('data/:uid', {
    handler: (req, rep) => {
      if (!req.params.uid) {
        return;
      }
      const { data, type } = database.getData({ uid: req.params.uid });
      if (!data || !type) {
        return rep
          .code(200)
          .header('Content-Type', 'application/json; charset=utf-8')
          .send({
            statusCode: 200,
            error: 'URL not found',
          });
      }
      rep
        .code(200)
        .header('Content-Type', 'application/json; charset=utf-8')
        .send({
          statusCode: 200,
          data,
          type
        });
    }
  });
}
