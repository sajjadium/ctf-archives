const express = require('express')
const app = express()
const private1Port = 1001

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/private1.js')
})

app.get('/private2', (req, res) => {
    res.sendFile(__dirname + '/private2.js')
})

// this port is only exposed locally
app.listen(private1Port, () => {
    console.log(`Listening on ${private1Port}`)
})