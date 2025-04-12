const express = require('express')
const path = require('path')
const crypto = require('crypto');
const bodyParser = require('body-parser');
const fs = require('fs/promises');
const app = express()

const port = 1337

app.use(bodyParser.json({ limit: '100kb' }));

const uploadsDir = path.join(__dirname, 'uploads_dir');

setTimeout(() => process.exit(0), 1000 * 60 * 15);


(async () => {
    await fs.mkdir(uploadsDir, { recursive: true });
    const items = await fs.readdir(uploadsDir);
    for(item of items) await fs.rm(path.join(uploadsDir, item), { recursive: true, force: true });

    const flagFile = await fs.readFile(path.join(__dirname, 'flag.txt'));
    uploadFile('admin', 'flag.txt', flagFile)
})();

const secret = () => crypto.randomBytes(32).toString('hex');

const users = [{ username: "admin", password: secret(), token: secret()}]

app.use("/", express.static(path.join(__dirname, 'public')));

app.post('/api/register', async (req, res) => {
    const { username, password } = req.body;
    
    if (!username || !password)
        return res.status(400).send('Username and password are required');

    const existingUser = users.find(u => u.username === username);
    if (existingUser) return res.status(400).send('User already exists');

    const token = secret();
    users.push({ username, password, token: token });

    const userFolder = crypto.createHash('sha256').update(username).digest('hex');
    const userDir = path.join(uploadsDir, userFolder);
    await fs.mkdir(userDir, { recursive: true });

    res.json({ username, token });
})

app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    
    if (!username || !password)
        return res.status(400).send('Username and password are required');

    const user = users.find(u => u.username === username && u.password === password);
    if (!user) return res.status(401).send('Invalid credentials');

    res.json({ username: user.username, token: user.token });
})

function encrypt(buffer, key, iv) {
    const cipher = crypto.createCipheriv('aes-256-ofb', key, iv);
    let encrypted = cipher.update(buffer);
    encrypted = Buffer.concat([encrypted, cipher.final()]);
    return encrypted;
}

const uploadFile = async (username, fileName, buffer) => { 

    const key = Buffer.from(process.env.ENCRYPTION_KEY, 'hex');
    const iv = Buffer.from(process.env.ENCRYPTION_IV, 'hex');

    if(buffer.length > 10000)
        return 'File too big';

    const userFolder = crypto.createHash('sha256').update(username).digest('hex');
    const userDir = path.join(uploadsDir, userFolder);
    await fs.mkdir(userDir, { recursive: true });

    const encryptedBuffer = encrypt(buffer, key, iv);

    await fs.writeFile(path.join(userDir, path.basename(fileName)), encryptedBuffer);
}

app.use((req, res, next) => {
    const token = req.headers["x-token"];
    const user = users.find(u => u.token === token);

    if (!user)
        return res.status(401).send('Unauthorized');

    req.user = user.username;
    next();
});

app.use("/files", express.static(path.join(__dirname, 'uploads_dir'))); // just for logged users


app.post('/api/upload', async (req, res) => {
    const { b64file, fileName } = req.body;
    
    if(!b64file || !fileName)
        return res.status(400).send('File is required');

    const buffer = Buffer.from(b64file, 'base64');
    
    const err = await uploadFile(req.user, fileName, buffer);
    if(err)
        res.status(400).send(err);

    res.send('ok');
});

app.get('/api/myfiles', async (req, res) => {
    const userFolder = crypto.createHash('sha256').update(req.user).digest('hex');
    const userDir = path.join(uploadsDir, userFolder);
    const files = await fs.readdir(userDir);
    res.json(files);
})

app.use((err, req, res, next) => {
    res.status(500).send('What?');
});

app.listen(port, () => {
  console.log(`App listening on port ${port}`)
})
