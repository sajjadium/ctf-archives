module.exports = async (fastify) => {
  fastify.get(':id', {
    handler: (req, rep) => {
      rep.sendFile('view.html');
    }
  })
}
