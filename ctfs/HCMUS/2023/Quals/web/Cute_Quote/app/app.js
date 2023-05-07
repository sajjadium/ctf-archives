const express = require('express')
const app = express()
const port = 3000

app.use(express.json())
app.use(express.static('css'))

app.get('/', (req, res) => {
  res.sendFile('./index.html', { root: __dirname })
})




const quotes = ['Insanity: doing the same thing expecting different results', '{{7*7}}', '<?php system("whoami"); ?>', '42 is the Answer to the Ultimate Question of Life, the Universe, and Everything']
app.get('/api/public/quote', (req, res) => {
  let quote = quotes[Math.floor(Math.random() * quotes.length)]
  res.send(quote)
})

app.get('/api/public/fake', (req, res) => {
  res.send("HMCSU-CFT{fake_flag}")
})

const flag = process.env.FLAG || "HCMUS-CTF{real_flag}"
app.get('/api/private/flag', (req, res) => {
  res.send(flag)
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})