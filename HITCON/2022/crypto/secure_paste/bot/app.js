const net = require('net')
const visit = require('./bot')
const dns = require('dns/promises')

const PORT = process.env.PORT || 7777
const REPORT_HOST = process.env.REPORT_HOST || 'localhost'

dns.lookup(REPORT_HOST).then(({ address }) => {
	const server = net.createServer(async socket => {
		if (!socket.remoteAddress.endsWith(address)) {
			// remoteAddress may be ipv4 mapped ipv6 address
			socket.end('Bad reporting host')
			return
		}
		socket.on('data', async data => {
			try {
				const url = data.toString().trim()
				socket.end('URL received')
				socket.destroy()

				console.log(`[+] Received: ${url}`)
				await visit(url)
				console.log(`[+] Visited: ${url}`)
			} catch (e) {
				console.log(e)
			}
		})
	})
	server.listen(PORT, () => {
		console.log('Bot socket server listening on port', PORT)
	})
})
