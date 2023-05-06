const crypto = require('crypto');
const express = require('express');
const app = express();

const notes = new Map();
const add = (note) => {
    const id = crypto
        .randomBytes(32)
        .toString('hex')

    notes.set(id, note);
    return id;
}

app.use(require('body-parser').urlencoded({ extended: false }));

app.get('/', (_req, res) => {
    res.type('html')
    res.end(`
        <link rel="stylesheet" href="/style.css" />
        <div class="container">
            <h1>Spyware Notes</h1>
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
    res.set('content-security-policy', 'script-src \'self\'');
    res.end(`
        <link rel="stylesheet" href="/style.css" />
        <div class="container">
            <h1>Note</h1>
            <div class="content">
                ${notes.get(id) ?? 'Note does not exist!'}
            </div>
            <br />
            <a>Previous note...</a>
        </div>
        <script src='/config.js'></script>
        <script src='/script.js'></script>
    `);
});

app.get('/config.js', (_req, res) => {
    res.type('javascript')
    res.end(`
        CONFIG = {
            analytics: 'https://log-api.newrelic.com/log/v1',
            key: '204db69d9bf5b2de59f84bbadda418805344NRAL',
        }
    `)
});

app.get('/script.js', (_req, res) => {
    res.type('javascript')
    res.end(`
        const previous = localStorage.previous;
        const current = window.location.toString();

        const a = document.querySelector('a');
        if (previous) {
            a.href = previous;
        } else {
            a.remove()
        }
        localStorage.previous = current;

        fetch(\`\${CONFIG.analytics}/?Api-Key=\${CONFIG.key}\`, {
            method: 'POST',
            headers: { 'content-type': 'application/javascript' },
            body: JSON.stringify({ previous: previous ?? '', current }),
            mode: 'no-cors',
        })
    `)
})

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
