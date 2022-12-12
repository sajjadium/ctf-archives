const fs = require('fs')
const crypto = require('crypto')
const prettier = require('prettier')
const { nextTick, exit } = require('process')
require('./fw')

const id = fs.readFileSync('./dist/id', 'utf-8').toString('utf-8').trim()
fs.unlinkSync('./dist/id')
prettier.resolveConfig(`${__dirname}/.prettierrc`).then(config => {
  const ret = prettier.format(fs.readFileSync(__filename, 'utf-8'), config)
  const o = crypto.createHash('sha256').update(Buffer.from(id, 'utf-8')).digest().toString('hex')
  fs.writeFileSync(`./dist/${id}`, o, 'utf-8')
  fs.writeFileSync('./dist/ret.js', ret, 'utf-8')
  nextTick(() => {
    throw new Error('No NextTick here!')
  })
  exit(0)
})
