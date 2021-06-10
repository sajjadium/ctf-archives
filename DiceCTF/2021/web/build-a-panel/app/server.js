/*
 *  @DICECTF 2021
 *  @AUTHOR Jim
 */

const admin_key = 'REDACTED'; // NOTE: The keys are not literally 'REDACTED', I've just taken them away from you :)
const secret_token = 'REDACTED'; 

const express = require('express');
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");
const sqlite3 = require('sqlite3');
const { v4: uuidv4 } = require('uuid');

const app = express();
const db = new sqlite3.Database('./db/widgets.db', (err) => {
    if(err){
        return console.log(err.message);
    }else{
        console.log('Connected to sql database');
    }
});

let query = `CREATE TABLE IF NOT EXISTS widgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    panelid TEXT,
    widgetname TEXT,
    widgetdata TEXT);`;
db.run(query);
query = `CREATE TABLE IF NOT EXISTS flag (
    flag TEXT
)`;
db.run(query, [], (err) => {
    if(!err){
        let innerQuery = `INSERT INTO flag SELECT 'dice{fake_flag}'`;
        db.run(innerQuery);
    }else{
        console.error('Could not create flag table');
    }
});

app.use(express.static(__dirname + '/public'));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(function(_req, res, next) {
    res.setHeader("Content-Security-Policy", "default-src 'none'; script-src 'self' http://cdn.embedly.com/; style-src 'self' http://cdn.embedly.com/; connect-src 'self' https://www.reddit.com/comments/;");
    res.setHeader("X-Frame-Options", "DENY");
    return next();
});
app.set('view engine', 'ejs');

app.get('/', (_req, res) => {
    res.render('pages/index');
});

app.get('/create', (req, res) => {
    const cookies = req.cookies;
    const queryParams = req.query;

    if(!cookies['panelId']){
        const newPanelId = queryParams['debugid'] || uuidv4();
    
        res.cookie('panelId', newPanelId, {maxage: 10800, httponly: true, sameSite: 'lax'});
    }

    res.redirect('/panel/');
});

app.get('/panel/', (req, res) => {
    const cookies = req.cookies;

    if(cookies['panelId']){
        res.render('pages/panel');
    }else{
        res.redirect('/');
    }
});

app.post('/panel/widgets', (req, res) => {
    const cookies = req.cookies;

    if(cookies['panelId']){
        const panelId = cookies['panelId'];

        query = `SELECT widgetname, widgetdata FROM widgets WHERE panelid = ?`;
        db.all(query, [panelId], (err, rows) => {
            if(!err){
                let panelWidgets = {};
                for(let row of rows){
                    try{
                        panelWidgets[row['widgetname']] = JSON.parse(row['widgetdata']);
                    }catch{
                        
                    }
                }
                res.json(panelWidgets);
            }else{
                res.send('something went wrong');
            }
        });
    }
});

app.get('/panel/edit', (_req, res) => {
    res.render('pages/edit');
});

app.post('/panel/add', (req, res) => {
    const cookies = req.cookies;
    const body = req.body;

    if(cookies['panelId'] && body['widgetName'] && body['widgetData']){
        query = `INSERT INTO widgets (panelid, widgetname, widgetdata) VALUES (?, ?, ?)`;
        db.run(query, [cookies['panelId'], body['widgetName'], body['widgetData']], (err) => {
            if(err){
                res.send('something went wrong');
            }else{
                res.send('success!');
            }
        });
    }else{
        console.log(cookies);
        console.log(body);
        res.send('something went wrong');
    }
});

const availableWidgets = ['time', 'weather', 'welcome'];

app.get('/status/:widgetName', (req, res) => {
    const widgetName = req.params.widgetName;

    if(availableWidgets.includes(widgetName)){
        if(widgetName == 'time'){
            res.json({'data': 'now :)'});
        }else if(widgetName == 'weather'){
            res.json({'data': 'as you can see widgets are not fully functional just yet'});
        }else if(widgetName == 'welcome'){
            res.json({'data': 'No additional data here but feel free to add other widgets!'});
        }
    }else{
        res.json({'data': 'error! widget was not found'});
    }
});

// This function is for admin bot setup
app.get('/admin/generate/:secret_token', (req, res) => {
    if(req.params['secret_token'] == admin_key){
        res.cookie('token', secret_token, {maxage: 10800, httponly: true, sameSite: 'lax'});
    }

    res.redirect('/');
});

app.get('/admin/debug/add_widget', async (req, res) => {
    const cookies = req.cookies;
    const queryParams = req.query;

    if(cookies['token'] && cookies['token'] == secret_token){
        query = `INSERT INTO widgets (panelid, widgetname, widgetdata) VALUES ('${queryParams['panelid']}', '${queryParams['widgetname']}', '${queryParams['widgetdata']}');`;
        db.run(query, (err) => {
            if(err){
                console.log(err);
                res.send('something went wrong');
            }else{
                res.send('success!');
            }
        });
    }else{
        res.redirect('/');
    }
});

app.listen(31337, () => {
    console.log('express listening on 31337')
});
