const crypto = require('crypto');
const express = require('express');
const app = express();

const state = { id: 0 };
const notes = new Map();
const add = (note) => {
    const id = crypto
        .createHash('sha256')
        .update(state.id.toString())
        .digest('hex');

    state.id += 1;

    notes.set(id, note);
    return id;
}

add(process.env.FLAG ?? 'flag missing!');

const sanitize = (text) => text.replace('<', '&lt;');

app.use(require('body-parser').urlencoded({ extended: false }));

app.get('/', (_req, res) => {
    res.type('html')
    res.end(`
        <link rel="stylesheet" href="/style.css" />
        <div class="container">
            <h1>Private Notes</h1>
            <form method="POST" action="/new">
                <input type="text" name="note" placeholder="Note" />
                <input type="submit" value="Submit" />
            </form>
        </div>
    `);
});

app.post('/new', (req, res) => {
    const note = (req.body.note ?? '').toString();
    const id = add(note);
    res.redirect(`/view/${id}`);
});

app.get('/view/:id', (req, res) => {
    const id = req.params.id;
    res.type('html');
    res.end(`
        <link rel="stylesheet" href="/style.css" />
        <div class="container">
            <h1>Note</h1>
            ${sanitize(notes.get(id) ?? 'Note does not exist!')}
        </div>
    `);
});

app.get('/style.css', (_req, res) => {
    res.end(`
        * {
            font-family: 'Helvetica Neue', sans-serif;
            box-sizing: border-box;
        }

        html, body { margin: 0; }

        .container {
            padding: 2rem;
            width: 90%;
            max-width: 900px;
            margin: auto;
        }

        input:not([type="submit"]) {
            width: 100%;
            padding: 8px;
            margin: 8px 0;
        }
    `);
});

app.listen(3000);
