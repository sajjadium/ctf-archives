(function (root, factory) {
	if (typeof define === 'function' && define.amd) {
		return define(['webcrypto', 'utils'], factory)
	} else if (typeof exports === 'object') {
		return (module.exports = factory(require('crypto').webcrypto, require('./utils')))
	} else {
		return (root.CryptoUtils = factory(crypto, utils))
	}
})(this, function (crypto, utils) {
	function CryptoUtils() {
		this.name ||= 'AES-GCM'
		this.additionalData ||= utils.textEncode('Secure Paste Encrypted Data')
	}
	CryptoUtils.prototype.urandom = function (len) {
		return crypto.getRandomValues(new Uint8Array(len))
	}
	CryptoUtils.prototype.genkey = async function (type) {
		return {
			type: type,
			data: new Uint8Array(
				await crypto.subtle.exportKey(
					type,
					await crypto.subtle.generateKey({ name: this.name, length: 128 }, true, ['encrypt', 'decrypt'])
				)
			)
		}
	}
	CryptoUtils.prototype.encrypt = async function (obj) {
		const ctx = { ...obj, name: this.name, additionalData: this.additionalData }
		const iv = this.urandom(12)
		ctx.iv = iv
		const key = await crypto.subtle.importKey(ctx.key.type, ctx.key.data, ctx, true, ['encrypt'])
		const ct = new Uint8Array(await crypto.subtle.encrypt(ctx, key, ctx.pt))
		return { ...obj, iv, ct }
	}
	CryptoUtils.prototype.decrypt = async function (obj) {
		const ctx = { ...obj, name: this.name, additionalData: this.additionalData }
		const key = await crypto.subtle.importKey(ctx.key.type, ctx.key.data, ctx, true, ['decrypt'])
		return new Uint8Array(await crypto.subtle.decrypt(ctx, key, ctx.ct))
	}
	return CryptoUtils
})