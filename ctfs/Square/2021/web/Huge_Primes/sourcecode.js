const express = require('express');
const bodyParser= require('body-parser');
const app = express();
const hugeProductOfPrimes = 22952152323332505688670761214671498225451684330137990990356473040741684014997701799009910066964917896400501477
const flag = ";)"
const correct = "Correct! Here is your flag: " + flag
const incorrect = "Incorrect factors! Try again"

// Constants
const PORT = 8080;
const HOST = '0.0.0.0';

app.set('view engine', 'ejs')


app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);

app.use(bodyParser.urlencoded({ extended: true }))

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html')
})

app.post('/factors', (req, res) => {
  a = req.body['a']
  b = req.body['b']
  if (a * b == hugeProductOfPrimes && a >= 2 && b >= 2) {
    res.render('index.ejs', { flag: correct })
    console.log()
  } else {
    res.render('index.ejs', { flag: incorrect })
  }
});
