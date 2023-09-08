import { Socket } from 'socket.io-client'

export interface Auth {
	username: string
	password: string
}
export interface ReceivedMessage {
	sender: string
	content: MessageContent
	time: string
}
export interface TextContent {
	type: 'text'
	text: string
}
export interface FileContent {
	type: 'file'
	filename: string
	uuid: string
}
type MessageContent = TextContent | FileContent

export interface FileUploadResponse {
	uuid: string
}

export class WrappedSocket {
	constructor(private socket: Socket) {}
	joinChannel(channel: string) {
		this.socket.emit('joinChannel', { channel })
	}
	leaveChannel(channel: string) {
		this.socket.emit('leaveChannel', { channel })
	}
	onMessage(callback: (message: ReceivedMessage) => void) {
		this.socket.on('message', callback)
	}
	offMessage(callback: (message: ReceivedMessage) => void) {
		this.socket.off('message', callback)
	}
	sendMessage(channel: string, content: MessageContent) {
		this.socket.emit('sendMessage', {
			channel,
			content
		})
	}
	uploadFile(filename: string, data: ArrayBuffer): Promise<FileUploadResponse> {
		return new Promise((resolve, reject) => {
			this.socket.emit('uploadFile', { filename, data })
			const success = (resp: FileUploadResponse) => {
				resolve(resp)
				cleanup()
			}
			const error = (err: any) => {
				reject(err)
				cleanup()
			}
			const cleanup = () => {
				this.socket.off('uploadFileResponse', success)
				this.socket.off('error', error)
			}
			this.socket.once('uploadFileResponse', success)
			this.socket.once('error', error)
		})
	}
}
