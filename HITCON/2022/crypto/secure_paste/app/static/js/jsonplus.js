(function (root, factory) {
	if (typeof define === 'function' && define.amd) {
		return define(['utils'], factory)
	} else if (typeof exports === 'object') {
		return (module.exports = factory(require('./utils')))
	} else {
		return (root.jsonplus = factory(utils))
	}
})(this, function (utils) {
	function serialize(obj) {
		return JSON.stringify(obj, (key, value) => {
			if (value?.buffer instanceof ArrayBuffer) {
				return {
					type: value.constructor.name,
					data: utils.arrayBufferToBase64(value.buffer)
				}
			}
			return value
		})
	}
	function deserialize(obj) {
		// I know this looks really sus, but the intended solution isn't about this at all
		return JSON.parse(obj, (key, value) => {
			if (value?.type in globalThis && value?.data) {
				return new globalThis[value.type](utils.base64ToArrayBuffer(value.data))
			}
			return value
		})
	}
	return { serialize, deserialize }
});