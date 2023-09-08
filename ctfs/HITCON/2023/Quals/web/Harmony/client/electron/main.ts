import { app, BrowserWindow, ipcMain, shell } from 'electron'
import path from 'node:path'
import xf from 'xfetch-js'
import fs from 'node:fs/promises'
import contentDisposition from 'content-disposition'
import { PersistedConfig } from './config'

// The built directory structure
//
// ├─┬─┬ dist
// │ │ └── index.html
// │ │
// │ ├─┬ dist-electron
// │ │ ├── main.js
// │ │ └── preload.js
// │
process.env.DIST = path.join(__dirname, '../dist')
process.env.PUBLIC = app.isPackaged ? process.env.DIST : path.join(process.env.DIST, '../public')

let mainWindow: BrowserWindow | null
// 🚧 Use ['ENV_NAME'] avoid vite:define plugin - Vite@2.x
const VITE_DEV_SERVER_URL = process.env['VITE_DEV_SERVER_URL']
const DEV = typeof VITE_DEV_SERVER_URL !== 'undefined'

const configPath = path.join(app.getPath('userData'), 'config.json')
const configPromise = PersistedConfig.from(configPath)

const SAFE_PROTOCOLS = ['http:', 'https:']

function createWindow() {
	mainWindow = new BrowserWindow({
		icon: path.join(process.env.PUBLIC, 'electron-vite.svg'),
		webPreferences: {
			preload: path.join(__dirname, 'preload.js'),
			nodeIntegration: false,
			contextIsolation: false
		}
	})

	// Test active push message to Renderer-process.
	mainWindow.webContents.on('did-finish-load', () => {
		mainWindow?.webContents.send('main-process-message', new Date().toLocaleString())
	})

	if (DEV) {
		mainWindow.loadURL(VITE_DEV_SERVER_URL)
		mainWindow.webContents.openDevTools()
	} else {
		mainWindow.loadFile(path.join(process.env.DIST, 'index.html'))
	}
	mainWindow.webContents.setWindowOpenHandler(({ url }) => {
		const { protocol } = new URL(url)
		if (SAFE_PROTOCOLS.includes(protocol)) {
			shell.openExternal(url)
		}
		return { action: 'deny' }
	})
	mainWindow.webContents.addListener('will-navigate', (event, url) => {
		event.preventDefault()
		const { protocol } = new URL(url)
		if (SAFE_PROTOCOLS.includes(protocol)) {
			shell.openExternal(url)
		}
	})
}

app.on('window-all-closed', () => {
	mainWindow = null
})
if (!DEV) {
	// no Chromium n-days please
	app.commandLine.appendSwitch('js-flags', '--jitless,--no-expose-wasm')
}
app.whenReady().then(createWindow)

ipcMain.handle('prompt', async (event, { message }) => {
	const promptWindow = new BrowserWindow({
		frame: false,
		width: 400,
		height: 200,
		modal: true,
		parent: mainWindow!,
		webPreferences: {
			preload: path.join(__dirname, 'preload.js'),
			nodeIntegration: false,
			contextIsolation: false
		}
	})
	promptWindow.loadFile(path.join(process.env.PUBLIC, 'prompt.html'))
	promptWindow.webContents.once('did-finish-load', () => {
		promptWindow.webContents.send('prompt-message', message)
	})
	promptWindow.webContents.ipc.handle('prompt-response', (_, { response }) => {
		promptWindow.close()
		event.sender.send('prompt-response', response)
	})
})
ipcMain.handle('download-to-temp', async (_, { url }) => {
	const temp = path.join(app.getPath('temp'), 'harmony')
	try {
		await fs.access(temp, fs.constants.F_OK)
	} catch {
		await fs.mkdir(temp)
	}
	const resp = await xf.get(url)
	const name = resp.headers.has('content-disposition')
		? contentDisposition.parse(resp.headers.get('content-disposition')!).parameters.filename
		: crypto.randomUUID()
	const file = path.join(temp, name)
	const buf = await resp.arrayBuffer()
	await fs.writeFile(file, Buffer.from(buf))
	return new URL(file, 'file:').href
})
configPromise.then(config => {
	ipcMain.handle('set-auth', (_, auth) => {
		config.setAuth(auth)
	})
	ipcMain.handle('get-auth', _ => {
		return config.getAuth()
	})
	ipcMain.handle('set-channels', (_, { username, channels }) => {
		config.setChannels(username, channels)
	})
	ipcMain.handle('get-channels', (_, { username }) => {
		return config.getChannels(username)
	})
	ipcMain.handle('get-config', _ => {
		return config.getConfig()
	})
})
