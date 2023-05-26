const express = require('express');
const app = express();
const sqlite3 = require('sqlite3');
const uuid = require('uuid');
const fs = require('fs');
const { parse } = require('csv-parse');

const flag = fs.readFileSync('./flag.txt', { encoding: 'utf8' }).trim();

app.use(express.urlencoded({ extended: true }));

const db = new sqlite3.Database(':memory:');

db.serialize(() => {
    db.run('CREATE TABLE jokes (id INTEGER PRIMARY KEY, joke TEXT)');

    const stmt = db.prepare('INSERT INTO jokes (id, joke) VALUES (?, ?)');

    // jokes from https://github.com/amoudgl/short-jokes-dataset/blob/master/data/reddit-cleanjokes.csv
    fs.createReadStream('./reddit-cleanjokes.csv').pipe(parse({ delimiter: ',' })).on('data', (row) => {
        stmt.run(row[0], row[1]);
    }).on('end', () => {
        stmt.finalize();
    });

    const flagTable = `flag_${uuid.v4().replace(/-/g, '_')}`;
    db.run(`CREATE TABLE IF NOT EXISTS ${flagTable} (flag TEXT)`);

    db.run(`INSERT INTO ${flagTable} (flag) VALUES ('${flag}')`);
});


app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.get('/search', (req, res) => {
    const { name } = req.query;

    if (!name) {
        return res.status(400).send({ err: 'Bad request' });
    }

    if (name.length > 6) {
        return res.status(400).send({ err: 'Bad request' });
    }

    db.all(`SELECT * FROM jokes WHERE joke LIKE '%${name}%'`, (err, rows) => {
        if (err) {
            console.error(err.message);
            return res.status(500).send('Internal server error');
        }

        return res.send(rows);
    });
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
