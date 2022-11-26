const crypto = require('crypto')

exports.Database = class Database {
	constructor() {
		this.store = new Map()
	}
	randid() {
		return crypto.randomBytes(16).toString('hex')
	}
	put(data) {
		const id = this.randid()
		this.store.set(id, data)
		return id
	}
	get(id) {
		return this.store.get(id)
	}
}
exports.setEqual = (a, b) => {
	return a.size === b.size && [...a].every(value => b.has(value))
}
