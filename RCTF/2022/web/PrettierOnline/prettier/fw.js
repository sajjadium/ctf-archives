const Module = require('module')
const oldRequire = Module.prototype.require
Module.prototype.require = function (id) {
  if (typeof id !== 'string') {
    throw new Error('Bye')
  }
  const isCore = Module.isBuiltin(id)
  if (isCore) {
    if (!/fs|path|util|os/.test(id)) {
      throw new Error('Bye, ' + id)
    }
  } else {
    id = Module._resolveFilename(id, this)
  }
  return oldRequire.call(oldRequire, id)
}
process.dlopen = () => {}
