const validatorFactory = require('@fastify/fast-json-stringify-compiler').SerializerSelector()()
const fastify = require('fastify')({
  logger: true,
})
const {v4: uuid} = require('uuid')
const FLAG = 'the old one'
const customValidators = Object.create(null, {}) // no more p.p.
const defaultSchema = {
  type: 'object',
  properties: {
    pong: {
      type: 'string',
    },
  },
}
fastify.get(
  '/',
  {
    schema: {
      response: {
        200: defaultSchema,
      },
    },
  },
  async () => {
    return {pong: 'hi'}
  }
)
fastify.get('/whowilldothis/:uid', async (req, resp) => {
  const {uid} = req.params
  const validator = customValidators[uid]
  if (validator) {
    return validator({[FLAG]: 'congratulations'})
  } else {
    return {msg: 'not found'}
  }
})

fastify.post('/register', {}, async (req, resp) => {
  // can only access from internal.
  const nid = uuid()
  const schema = Object.assign({}, defaultSchema, req.body)
  customValidators[nid] = validatorFactory({schema})
  return {route: `/whowilldothis/${nid}`}
})
fastify.listen({port: 3000, host: '0.0.0.0'}, function (err, address) {
  if (err) {
    fastify.log.error(err)
    process.exit(1)
  }
  // Server is now listening on ${address}
})
