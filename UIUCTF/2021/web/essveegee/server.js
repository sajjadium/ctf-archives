const fs = require('fs')
const crypto = require('crypto')
const childProcess = require('child_process')
const express = require('express')
const session = require('express-session')
const multer = require('multer')
const hcaptcha = require('hcaptcha')

const FSStore = require('./store.js')
const SESSION_DIR = '/app/sessions'

const app = express()
const port = 1337

app.use(express.urlencoded({ extended: false }))
app.use(session({
    secret: process.env.SECRET,
    resave: true,
    saveUninitialized: true,
    store: new FSStore({ dir: SESSION_DIR }),
    cookie: { secure: false }
}))

app.use((req, _res, next) => {
    if (!req.session.conversions) {
        fs.mkdirSync(`${SESSION_DIR}/${req.sessionID}/uploads`, { recursive: true })
        fs.mkdirSync(`${SESSION_DIR}/${req.sessionID}/output`, { recursive: true })
        req.session.conversions = {}
    }
    next()
})

const upload = multer({
    storage: multer.diskStorage({
        destination: (req, _file, cb) => cb(null, `${SESSION_DIR}/${req.sessionID}/uploads/`),
        filename: (_req, file, cb) => cb(null, crypto.createHash('sha256').update(file.originalname).digest('hex') + ".svg")
    }),
    limits: {
        files: 1,
        parts: 1,
        fields: 0,
        fileSize: 1024 * 1024 //1MB
    }
})

app.get('/', (_req, res) => {
    res.sendFile('/app/index.html')
})

const STATUS = { UPLOADED: 1, PROCESSING: 2, SUCCESS: 3, FAILURE: -1 }
app.post('/upload', upload.single('svg'), (req, res) => {
    const fileId = req.file.filename.split('.').slice(0, -1).join('.')
    req.session.conversions = {
        ...req.session.conversions,
        [fileId]: STATUS.UPLOADED
    }
    res.json({ uploaded: true, id: fileId })
})

app.get('/uploads', (req, res) => {
    res.json(req.session.conversions)
})

app.post('/convert', async (req, res) => {
    if (!req.body?.id) {
        res.status(400)
        res.end('No upload id :(')
        return
    }
    const fid = req.body.id
    if (!req.session?.conversions?.[fid]) {
        res.status(400)
        res.end('Invalid upload id :(')
        return
    }
    if (!process.env.DEBUG && req.header("X-ADMIN-TOKEN") !== process.env.SECRET) {
        if (!req.body?.['h-captcha-response']) {
            res.status(400)
            res.end('No hCaptcha token :(')
            return
        }
        const valid = (await hcaptcha.verify(process.env.HCAPTCHA_SECRET, req.body['h-captcha-response'])).success
        if (!valid) {
            res.status(400)
            res.end('Invalid hCaptcha token :(')
            return
        }
    }
    // move the flag to a super secret directory
    try {
        fs.rmdirSync(`${SESSION_DIR}/${req.sessionID}/flag`, { recursive: true })
    } catch { }
    try {
        const flagPath = `${SESSION_DIR}/${req.sessionID}/flag/${crypto.randomBytes(5).toString('hex').split('').join('/')}`
        fs.mkdirSync(flagPath, { recursive: true })
        fs.writeFileSync(`${flagPath}/flag.txt`, process.env.FLAG ?? 'flag{test_flag}')
    } catch { }

    req.session.conversions = {
        ...req.session.conversions,
        [fid]: STATUS.PROCESSING
    }
    res.redirect(`/convert/${fid}`)
    const svgPath = `${SESSION_DIR}/${req.sessionID}/uploads/${fid}.svg`
    const outPath = `${SESSION_DIR}/${req.sessionID}/output/${fid}.png`
    childProcess.execFile("node", ["bot.js", svgPath, outPath], (err, _stdout, _stderr) => {
        if (err)
            console.error(err)
        req.session.conversions = {
            ...req.session.conversions,
            [fid]: (err) ? STATUS.FAILURE : STATUS.SUCCESS
        }
        req.session.save()
    })
})

app.get('/convert/:fid', (req, res) => {
    if (req.session.conversions[req.params.fid] === STATUS.FAILURE) {
        res.type('text/plain')
        res.status(400)
        res.end('Error converting SVG :(')
    }
    else if (req.session.conversions[req.params.fid] === STATUS.SUCCESS) {
        res.type('image/png')
        res.sendFile(`${SESSION_DIR}/${req.sessionID}/output/${req.params.fid}.png`)
    }
    else if (req.session.conversions[req.params.fid] === STATUS.PROCESSING) {
        res.type('text/html')
        res.end(`
        <meta http-equiv="refresh" content="10;url=/convert/${encodeURIComponent(req.params.fid)}">
        <b>SVG conversion still processing... please wait</b>
        `)
    }
    else {
        res.type('text/plain')
        res.status(404)
        res.end('Not found')
    }
})

app.listen(port, () => {
    console.log(`app listening on port ${port}`)
})
