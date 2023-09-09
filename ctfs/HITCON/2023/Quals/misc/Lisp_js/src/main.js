const { lispEval } = require('./runtime')
const fs = require('fs')

const code = fs.readFileSync(process.argv[2], 'utf-8')
console.log(lispEval(code))
