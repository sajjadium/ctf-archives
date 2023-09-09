const express = require('express');
const { formidable } = require('formidable');
const mustache = require('mustache-express');
const { v4: uuidv4 } = require('uuid');
const https = require('https');
const fs = require('fs');
const app = express();


const port = process.env.PORT || 443;
const BOT_HOST = process.env.BOT_HOST || 'bot.internal';

const fileMetadata = new Map();

app.use(express.urlencoded({ extended: true }));
app.use((req, res, next) => {
    res.locals.baseURL = `${req.protocol}://${req.hostname}`;
    res.setHeader('Content-Security-Policy', `default-src 'none'; style-src ${res.locals.baseURL}/static/simple.css;`);
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'SAMEORIGIN');
    next();
});

app.engine('mustache', mustache());
app.set('view engine', 'mustache');

app.use('/static', express.static('static'));

app.get('/', (_, res) => {
    res.render('index');
});

app.post('/upload', (req, res) => {
    const form = formidable({
        maxFileSize: 1 * 1024 * 1024 // 1MB
    });
    form.parse(req, async (err, fields, files) => {
        if (err) {
            return res.render('index', { message: 'Upload failed' });
        }
        if (!files || !files.file) {
            return res.render('index', { message: 'No file uploaded' });
        }
        const file = files.file[0];
        let { originalFilename: name , mimetype } = file;

        const file_id = uuidv4();
        fileMetadata.set(file_id, { mimetype, name });
        fs.renameSync(file.filepath, `./uploads/${file_id}`);
        res.redirect(`/preview/${file_id}`);
    });
});

app.get('/file/:file_id', (req, res) => {
    const file_id = req.params.file_id;

    if (!fileMetadata.has(file_id)) {
        return res.status(404).send('File not found');
    }

    let { name, mimetype } = fileMetadata.get(file_id);

    if (req.query.download) {
        res.setHeader('Content-Type', 'application/octet-stream');
        res.setHeader('Content-Disposition', `attachment; filename="${name}"`);
        return res.sendFile(__dirname + `/uploads/${file_id}`)
    }

    res.setHeader('Content-Type', mimetype);
    return res.sendFile(__dirname + `/uploads/${file_id}`)
});

app.get('/preview/:file_id', (req, res) => {
    const file_id = req.params.file_id;

    if (!fileMetadata.has(file_id)) {
        return res.status(404).send('File not found');
    }

    const metadata = fileMetadata.get(file_id);
    res.setHeader('Content-Security-Policy', `default-src 'none'; style-src ${res.locals.baseURL}/static/simple.css; frame-src ${res.locals.baseURL}/file/${file_id}`);
    res.render('preview', { file_id, ...metadata });
});

app.get('/flag', (req, res) => {
    res.send(`<h1>FLAG</h1><iframe sandbox srcdoc="hitcon{${process.env.FLAG.split('').join('-')}}"></iframe>`);
});

app.get('/report', (_, res) => {
    res.render('report');
});

app.post('/report', (req, res) => {
    const data = req.body;

    if (!fileMetadata.has(data.file_id)) {
        return res.render('report', { message: 'File not found', ...data });
    }
    if (!data.token || !data.token.match(/^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$/)) {
        return res.render('report', { message: 'Token is not a valid uuid', ...data });
    }

    fetch(`https://${BOT_HOST}/visit?path=/preview/${data.file_id}&token=${data.token}`)
        .then(r => r.text())
        .then(message => res.render('report', { message }))
        .catch(() => res.render('report', { message: 'Something went wrong', ...data }));
});


https.createServer({
    key: fs.readFileSync('/opt/certificates/privkey.pem'),
    cert: fs.readFileSync('/opt/certificates/fullchain.pem')
}, app).listen(port, () => {
    console.log(`Express app listening at https://localhost:${port}`)
});

