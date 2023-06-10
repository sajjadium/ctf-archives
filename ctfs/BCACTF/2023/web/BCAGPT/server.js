const express = require('express');
const { readFileSync, read } = require('fs');
const sqlite3 = require('sqlite3').verbose();
const hbs = require('hbs');
const bodyParser = require('body-parser');

let fp = readFileSync([46,47,102,47,108,47,97,47,103,47,102,108,97,103,46,116,120,116].map((x) => 
    String.fromCharCode(x)
).join('')).toString();

const port = 3000;
const app = express();
app.set('view engine', 'hbs');
app.set('views', __dirname + '/pages');
app.use(express.static(__dirname + '/public'));

const urlencodedParser = bodyParser.urlencoded({ extended: false })

let db;

db = new sqlite3.Database(__dirname + '/db/ai_training.db', (err) => {
    if (err) {
        console.error(err.message);
    } else {
        db.serialize(() => {
            db.run(`DROP TABLE IF EXISTS response`);
        });
    }
});

let createRespTable = readFileSync('./query/create_train.sql').toString();
let fillRespTable = readFileSync('./query/train_train.sql').toString();
db.serialize(() => {
    db.run(createRespTable);
});

db.serialize(() => {
    db.run(fillRespTable, fp);
});


app.get('/', async (req, res) => {
    res.render('index');
});

app.get('/css/style.css', (req, res) => {res.sendFile(__dirname + '/css/style.css');});
app.post('/ai', urlencodedParser, (req, res) => {
    let kwds = req.body.query ?? '%';
    let msgs = [{author: 'you', message: kwds=="%" ? 'No query found' : kwds}];
    
    db.serialize(() => {
        db.get(`SELECT response_text FROM response WHERE response_keywds !='${kwds}' ORDER BY resp_order, RANDOM() LIMIT 1`, (err, row) => {
            if (err) {
                console.error(err.message);
                res.render('index', {error: err.message});
            } else {
                let resp = row?.response_text?.replace("{}",req.body.query) ?? "AI brain overheated";
                msgs.push({author: 'BCAGPT', message: resp});
                
                res.render('index', {
                    messages: msgs
                });
            }
            return;
        });
    });

    return
});

app.listen(port, () => {
    console.log(`Listening at http://localhost:${port}`);
});