const express = require('express')
const session = require('express-session')
const crypto = require('crypto')
const fs = require('fs')
const fsp = require('fs/promises')
const yaml = require('js-yaml')
const cp = require('child_process')
const http = require('http')
const path = require('path')

// this is not a part of the challenge, just for isolating the challenge instance
const HTTP_USERNAME = process.env.HTTP_USERNAME
const HTTP_PASSWORD = process.env.HTTP_PASSWORD

const LOGIN_SYS = process.env.LOGIN_SYS || 'http://127.0.0.1:5000'
const PORT = process.env.PORT || 3000
const PRIVILEGE_DIR = path.join(__dirname, 'privilege')
const GUEST_PRIVILEGE = yaml.load(fs.readFileSync(path.join(PRIVILEGE_DIR, 'guest.yaml'), 'utf8'))

const app = express()
app.set('view engine', 'ejs')
app.set('views', path.join(__dirname, 'views'))

if (HTTP_USERNAME && HTTP_PASSWORD) {
	// this is not a part of the challenge, just for isolating the challenge instance
	app.use((req, res, next) => {
		const auth = req.headers.authorization
		if (!auth) {
			res.set('WWW-Authenticate', 'Basic realm="Login required"')
			return res.status(401).send('Login required')
		}
		const [username, password] = Buffer.from(auth.slice(6), 'base64').toString().split(':')
		if (username !== HTTP_USERNAME || password !== HTTP_PASSWORD) {
			res.set('WWW-Authenticate', 'Basic realm="Login required"')
			return res.status(401).send('Login required')
		}
		next()
	})
}

app.use(express.static(path.join(__dirname, 'public')))
app.use(
	session({
		secret: crypto.randomBytes(20).toString('hex'),
		resave: true,
		saveUninitialized: false
	})
)

app.use((req, res, next) => {
	req.session.privilegeLevel ||= 'guest'
	fsp.readFile(path.join(PRIVILEGE_DIR, `${req.session.privilegeLevel}.yaml`), 'utf8')
		.then(data => {
			req.privilege = yaml.load(data)
			next()
		})
		.catch(err => {
			console.error(err)
			req.privilege = GUEST_PRIVILEGE
			next()
		})
})

const accessRequired = name => (req, res, next) => {
	if (req.privilege.access[name]) {
		next()
	} else {
		res.status(403).json({ error: 'Access denied' })
	}
}

for (const proxyiedPath of ['/login', '/register', '/change_password']) {
	app.post(proxyiedPath, accessRequired(proxyiedPath.slice(1)), (req, res) => {
		const hreq = http
			.request(
				new URL(proxyiedPath, LOGIN_SYS).href,
				{
					method: req.method,
					headers: req.headers
				},
				hres => {
					const bufs = []
					hres.on('data', buf => {
						bufs.push(buf)
					})
					hres.on('end', () => {
						const body = Buffer.concat(bufs).toString()
						try {
							const data = JSON.parse(body)
							if (data.success && data.data) {
								req.session.username = data.data.username
								req.session.privilegeLevel = data.data.privilegeLevel
							}
						} catch {}
						res.type('json').send(body)
					})
				}
			)
			.on('error', err => {
				res.status(500).json({ error: 'Internal server error' })
			})
		req.pipe(hreq)
	})
}

app.use((req, res, next) => {
	res.locals = {
		username: req.session.username,
		privilegeLevel: req.privilege.privilegeLevel,
		access: req.privilege.access
	}
	next()
})

app.get('/', accessRequired('index'), (req, res) => {
	res.render('index')
})

app.get('/register', accessRequired('register'), (req, res) => {
	res.render('register')
})

app.get('/login', accessRequired('login'), (req, res) => {
	res.render('login')
})

app.get('/profile', accessRequired('profile'), (req, res) => {
	res.render('profile')
})

app.get('/logout', accessRequired('logout'), (req, res) => {
	req.session.destroy()
	res.redirect('/')
})

app.get('/flag', accessRequired('flag'), (req, res) => {
	cp.execFile('/readflag', (err, stdout, stderr) => {
		if (err) {
			return res.status(500).type('text').send('Internal server error')
		}
		const h = crypto.createHash('sha256').update(stdout).digest('hex')
		return res.type('text').send(`Well done, this is a hashed flag for you: ${h}`)
	})
})

app.listen(PORT, () => {
	console.log(`Server listening on http://localhost:${PORT}`)
})
