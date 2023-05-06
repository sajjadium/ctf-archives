const express = require('express');
const path = require('path');
const createError = require('http-errors');

const app = express();

app.use(express.json())

let checkin = require('./routes/checkin');
let upgrades = require('./routes/upgrades');
app.use("/", checkin);
app.use("/upgrades", upgrades);
app.use(express.static(path.join(__dirname, 'public')));

app.use(function(req, res, next) {
  res.status(404);
  res.json(createError(404));
});

app.listen(3000, () => console.log('Running on port 3000'));
