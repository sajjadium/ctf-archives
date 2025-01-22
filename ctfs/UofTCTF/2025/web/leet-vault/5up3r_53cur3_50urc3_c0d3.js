const express = require('express');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');
const ejs = require('ejs');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const SECRET_FLAG = require('secret-flag')
const app = express();
const PORT = process.env.PORT || 1337;

const rsaKeys = JSON.parse(fs.readFileSync('rsa_keys.json'));
const PRIVATE_KEY = rsaKeys.private_key;
const PUBLIC_KEY = rsaKeys.public_key;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static('public'));
app.set('view engine', 'ejs');

app.get('/', (req, res) => {
    res.render('index');
});

app.post('/login', (req, res) => {
    const username = req.body.username;

    if (!username) {
        return res.status(400).render('index', { error: 'Us3rn4m3 15 r3qu1r3d.' });
    }

    // Ch3ck f0r 4dm1n us3rn4m3
    if (username.toLowerCase() === '4dm1n') {
        // D0n'7 4ll0w
        return res.status(403).render('accessDenied', { message: 'N1c3 try!' });
    } else {
        // G3n3r473 JWT f0r r3gul4r us3r
        const token = jwt.sign({ username: username }, PRIVATE_KEY, { algorithm: 'RS256' });
        res.cookie('token', token, { httpOnly: true });
        return res.render('index', { success: `W3lc0m3 ${username}! Y0u 4r3 n0t 4n 4dm1n.` });
    }
});

app.get('/1337_v4u17', (req, res) => {
    const token = req.cookies ? req.cookies.token : null;
    if (!token) {
        return res.status(401).render('accessDenied', { message: 'un4u7h0r1z3d 4cc355. y0u mu57 b3 4n 4dm1n!' });
    }

    try {
        const decoded = jwt.verify(token, PUBLIC_KEY, { algorithms: ['RS256'] });
        if (decoded.username !== '4dm1n') {
            return res.status(403).render('accessDenied', { message: 'F0rb1dd3n: Y0u d0 n07 h4v3 4cc355 t0 th15 p4g3.' });
        }

        const fileQuery = req.query.file;
        if (fileQuery) {
            const filePath = path.join(__dirname, fileQuery);
            fs.readFile(filePath, 'utf8', (err, data) => {
                if (err) {
                    return res.render('accessDenied', { message: 'F1l3 n07 f0und 0r 1n4ccess1bl3.' });
                }
                const filename = path.basename(filePath);
                res.render('viewFile', { filename: filename, fileContent: data });
            });
        } else {
            const vaultDir = path.join(__dirname, 'vault');
            fs.readdir(vaultDir, (err, files) => {
                if (err) {
                    return res.render('accessDenied', { message: 'C0uld n0t l15t f1l3s.' });
                }
                const filePathPrefix = 'vault/';
                res.render('admin', { files: files, filePathPrefix: filePathPrefix });
            });
        }

    } catch (err) {
        return res.status(401).render('accessDenied', { message: '1nv4l1d T0k3n.' });
    }
});

app.listen(PORT, () => {
    console.log(`53rv3r 15 runn1n6 0n p0r7 ${PORT}`);
});
