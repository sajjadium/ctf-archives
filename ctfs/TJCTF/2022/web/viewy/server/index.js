const express = require('express');
const fs = require('fs');
const { v4: uuidv4 } = require('uuid');
const path = require('path');

const app = express();
app.set('view engine', 'ejs');

app.use(express.urlencoded({ extended: false }));

app.get('/', (req, res) => {
  res.render('index');
});

app.post('/', (req, res) => {
  const id = uuidv4();
  const { content } = req.body;
  const fileName = path.join(__dirname, 'views/uploads', `${id}.ejs`);
  fs.writeFileSync(fileName, content);
  return res.redirect('/views/' + id);
});

app.get('/views/:id', (req, res) => {
  if (
    fs.existsSync(path.join(__dirname, 'views/uploads', `${req.params.id}.ejs`))
  ) {
    res.render('view', { id: req.params.id });
  } else {
    res.status(404).send('Not found');
  }
});

app.listen(3000, '0.0.0.0', () => {
  console.log('listening on port 3000');
});
