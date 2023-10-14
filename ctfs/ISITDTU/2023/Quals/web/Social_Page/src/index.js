const express = require('express');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const { merge } = require('lodash');
const fs = require('fs');

const app = express();
app.use(express.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use("/", express.static(__dirname + "/static"));
app.use(cookieParser());

const defaultAccount = 
{
  username: 'Admin',
  password: 'Admin@123'
}
let i = 0;

app.post('/login', (req, res, next) => {
  try{
    const username = req.body.username ?? '';
    const password = req.body.password ?? '';

    if (username === defaultAccount.username && password === defaultAccount.password) {
      const prime_token = jwt.sign({isPrime: true}, process.env.JWT_SECRET_KEY || 'pentest');
      res.cookie('jwt', prime_token);
      res.redirect('/index.html')
    }
    else res.send('Fail');
    return;
  } catch (error){
    writeLog(error.message)
    res.send('Fail');
  }
});

const defaultTweet = [{ thoughts: 'Sometimes we shouldn\'t think too much', name: 'Thangxamlo'}]

const addThought = (thoughts, name) => {
  if (!thoughts) {
    throw new Error('Required thoughts');
  }

  if (!name) {
    throw new Error('Required Name');
  }

  if (containsRestrictedWords(thoughts)) {
    throw new Error('Thought invalid');
  }

  if (containsRestrictedWords(name)) {
    throw new Error('Name invalid');
  }

  if (thoughts.length > 30) {
    throw new Error("Error:" + thoughts);
  }

  if (name.length > 10) {
    throw new Error(name);
  }

  if (name === thoughts) {
    throw new Error('Must not be the same' + name);
  }

  defaultTweet.push({ thoughts, name })
}

const environment = {};

const writeLog = (message) => {
  try {
    i++;

    fs.writeFile(`error${i}${environment?.local ? '.js' : '.txt'}`, message, (err) => {
      if (err) {
        console.error('Error writing to the file:', err);
      } else {
        console.log(`Error message has been written`);
      }
    });
  } catch (e) {
    console.error('Error writing to the file:', err);
  }
}

const containsRestrictedWords = (inputString) => {
  const restrictedWords = ['abc', 'export', 'fuck', 'default', 'corn'];

  for (const word of restrictedWords) {
    if (inputString.includes(word)) {
      return true;
    }
  }

  return false;
}

app.post('/save', (req, res) => {
  try {
    const prime_token = req.cookies['jwt'];
    if (jwt.verify(prime_token, process.env.JWT_SECRET_KEY || 'pentest')){
      const thoughts = req.body.thoughts ?? '';
      const name = req.body.name ?? '';

      try {
        addThought(thoughts, name)
        res.json(defaultTweet);
      } catch (error) {
        writeLog(error.message)
        res.status(401)
      }
      res.status(401)
    } else{
      writeLog('Something Wrong')
      return res.status(401)
    }
  } catch (error) {
    writeLog(error.message)
    return res.status(401).send(error);
  }
});

app.get('/get', (req, res) => {
  try {
    const prime_token = req.cookies['jwt'];
    if (jwt.verify(prime_token, process.env.JWT_SECRET_KEY || 'pentest')){
      const thought = req.query.thought;

      res.json(defaultTweet.find(({ thoughts }) => thoughts === thought))
    } else{
      writeLog('Something Wrong')
      return res.status(401)
    }
  } catch (error) {
    writeLog(error.message)
    return res.status(401).send(error);
  }
});

app.get('/log', (req, res, next) => {
  try{
    const query1 = req.query.q1;
    res.sendFile(`${query1}${environment?.local ? '.js' : '.txt'}`)
  } catch (error){
    res.send(error);
  }
});

app.get('/logs', (req, res, next) => {
  try{
    const query1 = req.query.q1;
    const query2 = req.query.q2;
    fs.readFile(`error${query1}${environment?.local ? '.js' : '.txt'}`, 'utf8', (err, data) => {
      if (err) {
        console.error('Error reading the JSON file:', err);
        writeLog('Something went wrong')
        return;
      }
    
      try {
        const file1 = JSON.parse(data);

        fs.readFile(`error${query2}${environment?.local ? '.js' : '.txt'}`, 'utf8', (e, data2) => {
          if (e) {
            console.error('Error reading the JSON file:', e);
            writeLog('Something went wrong')
            return;
          }
        
          try {
            const file2 = JSON.parse(data2);
            const mergedObject = merge(file2, merge({}, file1));
            res.json(mergedObject);
          } catch (parseError) {
            console.error('Error parsing JSON:', parseError);
            writeLog('Something went wrong')
          }
        });
      } catch (parseError) {
        console.error('Error parsing JSON:', parseError);
        writeLog('Something went wrong')
      }
    });
  } catch (error){
    res.send(error);
    writeLog('Something went wrong')
  }
});


app.post('/errorlog', function (req, res, next) {
  try {
    const prime_token = req.cookies['jwt'];
    if (jwt.verify(prime_token, process.env.JWT_SECRET_KEY || 'pentest')){
      const query1 = req.query.q1;
      const query2 = req.query.q2;
      const errorlog1 = require(`./error${query1}${environment?.local ? '.js' : '.txt'}`)
      const errorlog2 = require(`./error${query2}${environment?.local ? '.js' : '.txt'}`)
      res.json(merge(errorlog1.all(), errorlog2.all()));
    } else{
      writeLog('Something went wrong')
      return res.status(401).send(error);
    }
  } catch (error) {
    writeLog('Something went wrong')
    return res.status(401).send(error);
  }
})

app.listen(3000, () => {
  console.log('listening on port 3000');
});