import { z } from 'zod'
import fs from 'node:fs/promises'

const AuthSchema = z
	.object({
		username: z.string(),
		password: z.string()
	})
	.optional()
const ChannelsSchema = z.record(z.boolean())
const ChannelsByUsernameSchema = z.record(ChannelsSchema)
const ConfigSchema = z.object({
	auth: AuthSchema,
	channels: ChannelsByUsernameSchema,
	serverUrl: z.string(),
	defaultChannel: z.string()
})
export type Auth = z.infer<typeof AuthSchema>
export type Channels = z.infer<typeof ChannelsSchema>
export type ChannelsByUsername = z.infer<typeof ChannelsByUsernameSchema>
export type Config = z.infer<typeof ConfigSchema>

const typeSafeAssign: <T extends object>(...args: T[]) => T = (...args) => Object.assign(args[0], ...args.slice(1))
export class PersistedConfig {
	constructor(private path: string, private config: Config) {
		this.save()
	}
	async save() {
		return fs.writeFile(this.path, JSON.stringify(this.config))
	}
	setAuth(auth: z.infer<typeof AuthSchema>) {
		this.config.auth = AuthSchema.parse(auth)
		this.save()
	}
	getAuth() {
		return this.config.auth
	}
	setChannels(username: string, channels: z.infer<typeof ChannelsSchema>) {
		if (!this.config.channels[username]) this.config.channels[username] = {}
		typeSafeAssign(this.config.channels[username], ChannelsSchema.parse(channels))
		this.save()
	}
	getChannels(username: string) {
		return this.config.channels[username]
	}
	getConfig() {
		return this.config
	}
	static async from(path: string) {
		try {
			const data = JSON.parse(await fs.readFile(path, 'utf-8'))
			return new PersistedConfig(path, data)
		} catch {
			return new PersistedConfig(path, {
				channels: {},
				serverUrl: 'http://localhost:3000',
				defaultChannel: 'general'
			})
		}
	}
}
