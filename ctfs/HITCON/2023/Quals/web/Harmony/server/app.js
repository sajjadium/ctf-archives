const express = require('express')
const socketio = require('socket.io')
const http = require('http')
const Database = require('better-sqlite3')
const crypto = require('crypto')

const PORT = process.env.PORT || 3000
const DB_FILE = process.env.DB_FILE || '/tmp/db.sqlite3'

const app = express()
app.use(express.json())
app.use((req, res, next) => {
	res.set('Access-Control-Allow-Origin', '*')
	res.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
	res.set('Access-Control-Allow-Headers', 'Content-Type')
	if (req.method === 'OPTIONS') {
		return res.status(200).end()
	}
	next()
})
const server = http.createServer(app)
const io = socketio(server, {
	cors: {
		origin: '*',
		methods: ['GET', 'POST', 'OPTIONS'],
		allowedHeaders: ['Content-Type']
	}
})

const db = new Database(DB_FILE)
db.pragma('journal_mode = WAL')
db.exec(`
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    channel TEXT NOT NULL,
    content TEXT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS files (
	uuid TEXT PRIMARY KEY,
	uploader_id INTEGER NOT NULL,
	filename TEXT NOT NULL,
	data BLOB NOT NULL,
	time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (uploader_id) REFERENCES users(id)
);
`)
const insertUser = db.prepare('INSERT INTO users (username, password) VALUES (?, ?)')
const selectUser = db.prepare('SELECT id, username FROM users WHERE username = ? AND password = ?')
const selectFile = db.prepare('SELECT filename, data FROM files WHERE uuid = ?')
const insertMessage = db.prepare('INSERT INTO messages (sender_id, channel, content, time) VALUES (?, ?, ?, ?)')
const insertFile = db.prepare('INSERT INTO files (uuid, uploader_id, filename, data, time) VALUES (?, ?, ?, ?, ?)')

app.post('/register', (req, res) => {
	const { username, password } = req.body
	if (!username || !password) {
		return res.status(400).json({ error: 'username and password required' })
	}
	if (typeof username !== 'string' || typeof password !== 'string') {
		return res.status(400).json({ error: 'username and password must be string' })
	}
	if (username.length < 8) {
		return res.status(400).json({ error: 'username must be at least 8 characters' })
	}
	if (password.length < 8) {
		return res.status(400).json({ error: 'password must be at least 8 characters' })
	}
	try {
		insertUser.run(username, password)
		res.json({ success: true })
	} catch (e) {
		res.status(400).json({ error: e.message })
	}
})
app.post('/login', (req, res) => {
	const { username, password } = req.body
	if (!username || !password) {
		return res.status(400).json({ error: 'username and password required' })
	}
	if (typeof username !== 'string' || typeof password !== 'string') {
		return res.status(400).json({ error: 'username and password must be string' })
	}
	const row = selectUser.get(username, password)
	if (!row) {
		return res.status(400).json({ error: 'invalid username or password' })
	}
	res.json({ success: true })
})
app.get('/file/:uuid', (req, res) => {
	const { uuid } = req.params
	const row = selectFile.get(uuid)
	if (!row) {
		return res.status(404).json({ error: 'file not found' })
	}
	res.attachment(row.filename)
	res.send(row.data)
})

io.use((socket, next) => {
	const { username, password } = socket.handshake.auth
	const row = selectUser.get(username, password)
	if (!row) return next(new Error('Invalid username or password'))
	socket.userid = row['id']
	socket.username = row['username']
	next()
})
io.on('connection', async socket => {
	socket.on('joinChannel', async ({ channel }) => {
		if (typeof channel !== 'string') {
			return socket.emit('error', 'channel must be string')
		}
		socket.join(channel)
	})
	socket.on('leaveChannel', async ({ channel }) => {
		if (typeof channel !== 'string') {
			return socket.emit('error', 'channel must be string')
		}
		socket.leave(channel)
	})
	socket.on('sendMessage', async ({ channel, content }) => {
		if (typeof channel !== 'string') {
			return socket.emit('error', 'channel must be string')
		}
		if (!content) {
			return socket.emit('error', 'content required')
		}
		const jsonContent = JSON.stringify(content)
		if (jsonContent.length > 1024) {
			return socket.emit('error', 'content too long')
		}
		const time = new Date().toISOString()
		insertMessage.run(socket.userid, channel, jsonContent, time)

		const msgObj = { sender: socket.username, channel, content, time }
		io.to(channel).emit('message', msgObj)
	})
	socket.on('uploadFile', async ({ filename, data }) => {
		if (typeof filename !== 'string') {
			return socket.emit('error', 'filename must be string')
		}
		if (!(data instanceof Buffer)) {
			return socket.emit('error', 'data must be Buffer')
		}
		if (data.byteLength > 1024 * 1024) {
			console.log(data.byteLength, 'too large')
			return socket.emit('error', 'data too large')
		}
		const uuid = crypto.randomUUID()
		const time = new Date().toISOString()
		insertFile.run(uuid, socket.userid, filename, data, time)
		socket.emit('uploadFileResponse', { uuid })
	})
})

server.listen(PORT, () => {
	console.log(`Listening on port ${PORT}`)
})
