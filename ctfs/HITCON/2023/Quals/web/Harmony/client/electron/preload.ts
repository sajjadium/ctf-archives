import electron from 'electron'
import { Auth, Channels, Config } from './config'

const api = {
	async prompt(message: string): Promise<string> {
		await electron.ipcRenderer.invoke('prompt', {
			message
		})
		return new Promise(resolve => {
			electron.ipcRenderer.once('prompt-response', (_, response) => {
				resolve(response)
			})
		})
	},
	promptResponse(response: string) {
		electron.ipcRenderer.invoke('prompt-response', {
			response
		})
	},
	registerPromptMessage(callback: (message: string) => void) {
		electron.ipcRenderer.once('prompt-message', (_, message) => {
			callback(message)
		})
	},
	downloadToTemp(url: string): Promise<string> {
		return electron.ipcRenderer.invoke('download-to-temp', {
			url
		})
	},
	setAuth(auth: Auth | undefined) {
		electron.ipcRenderer.invoke('set-auth', auth)
	},
	async getAuth(): Promise<Auth> {
		return electron.ipcRenderer.invoke('get-auth')
	},
	setChannels(username: string, channels: Channels) {
		electron.ipcRenderer.invoke('set-channels', {
			username,
			channels
		})
	},
	async getChannels(username: string): Promise<Channels | null> {
		return electron.ipcRenderer.invoke('get-channels', {
			username
		})
	},
	async getConfig(): Promise<Config> {
		return electron.ipcRenderer.invoke('get-config')
	}
}

declare global {
	interface Window {
		api: typeof api
	}
}
window.api = api
