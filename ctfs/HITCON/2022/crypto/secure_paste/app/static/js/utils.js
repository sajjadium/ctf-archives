(function (root, factory) {
	if (typeof define === 'function' && define.amd) {
		return define([], factory)
	} else if (typeof exports === 'object') {
		return (module.exports = factory())
	} else {
		return (root.utils = factory())
	}
})(this, function () {
	// copied from https://stackoverflow.com/a/38858127
	function arrayBufferToBase64(buffer) {
		var binary = ''
		var bytes = new Uint8Array(buffer)
		var len = bytes.byteLength
		for (var i = 0; i < len; i++) {
			binary += String.fromCharCode(bytes[i])
		}
		return btoa(binary)
	}
	function base64ToArrayBuffer(base64) {
		var binary_string = atob(base64)
		var len = binary_string.length
		var bytes = new Uint8Array(len)
		for (var i = 0; i < len; i++) {
			bytes[i] = binary_string.charCodeAt(i)
		}
		return bytes.buffer
	}
	function textEncode(obj) {
		return new TextEncoder().encode(obj)
	}
	function textDecode(obj) {
		return new TextDecoder().decode(obj)
	}
	return { arrayBufferToBase64, base64ToArrayBuffer, textEncode, textDecode }
});