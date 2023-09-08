let su: string | undefined
let dc: string | undefined
if (typeof window.api !== 'undefined') {
	const config = await window.api.getConfig()
	su = config.serverUrl
	dc = config.defaultChannel
}
export const serverUrl = su ?? 'http://localhost:3000'
export const defaultChannel = dc ?? 'general'
