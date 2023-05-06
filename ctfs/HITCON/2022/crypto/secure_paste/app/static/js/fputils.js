((function (root, factory) {
	if (typeof define === 'function' && define.amd) {
		return define([], factory)
	} else if (typeof exports === 'object') {
		return (module.exports = factory())
	} else {
		return (root.fputils = factory())
	}
})(this, function () {
	function acompose(...fns) {
		// async function composition
		fns.reverse()
		return async x => {
			for (const f of fns) {
				x = await f(x)
			}
			return x
		}
	}
	return { acompose }
}));