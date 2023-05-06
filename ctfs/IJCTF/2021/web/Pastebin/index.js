const express = require('express')
const api = require('./api.js')
const report = require('./report.js')

const app = express()
app.use(express.static('public'))
app.use(express.urlencoded({
  extended: true
}))



app.post('/api/create',api.createPaste)
app.get('/api/get/:id',api.getPaste)
app.post('/api/report',report.report)

app.listen(1337,'0.0.0.0', () => {
  console.log(`Listening`)
})
