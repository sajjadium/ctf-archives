function allKeys(obj) {
	let keys = []
	while (obj !== null) {
		keys = keys.concat(Object.getOwnPropertyNames(obj))
		keys = keys.concat(Object.keys(Object.getOwnPropertyDescriptors(obj)))
		obj = Object.getPrototypeOf(obj)
	}
	return [...new Set(keys)]
}
function escapeHTML(s) {
	return String(s)
		.replace(/&/g, '&amp;')
		.replace(/</g, '&lt;')
		.replace(/>/g, '&gt;')
		.replace(/"/g, '&quot;')
		.replace(/'/g, '&#039;')
}
function html(htmls, ...vals) {
	let result = ''
	for (let i = 0; i < htmls.length; i++) {
		result += htmls[i]
		result += escapeHTML(vals[i] ?? '')
	}
	return result
}
function hardening() {
	const fnCons = [function () {}, async function () {}, function* () {}, async function* () {}].map(
		f => f.constructor
	)
	for (const c of fnCons) {
		Object.defineProperty(c.prototype, 'constructor', {
			get: function () {
				throw new Error('Nope')
			},
			set: function () {
				throw new Error('Nope')
			},
			configurable: false
		})
	}
	const cons = [Object, Array, Number, String, Boolean, Date, RegExp, Promise, Symbol, BigInt].concat(fnCons)
	for (const c of cons) {
		Object.freeze(c)
		Object.freeze(c.prototype)
	}
}
self.addEventListener('message', function (event) {
	if (event.data.type === 'init') {
		const canvas = event.data.canvas
		const ctx = canvas.getContext('2d')

		// taken from https://github.com/lionleaf/dwitter/blob/83cd600567692babb13ffec314c6066c4dfa04e4/dwitter/templates/dweet/dweet.html#L267-L270
		const R = function (r, g, b, a) {
			a = a === undefined ? 1 : a
			return 'rgba(' + (r | 0) + ',' + (g | 0) + ',' + (b | 0) + ',' + a + ')'
		}

		const customArgs = ['c', 'x', 't', 'S', 'C', 'T', 'R']
		const argNames = customArgs.concat(allKeys(self))
		// run user code in an isolated environment
		const fn = Function(...argNames, event.data.code)
		const callUserFn = t => {
			try {
				fn.apply(Object.create(null), [canvas, ctx, t, Math.sin, Math.cos, Math.tan, R])
			} catch (e) {
				console.error('User function error', e)
				postMessage({
					type: 'error',
					content: html`<div>
						<h2>Script Error</h2>
						<pre>${e.message ?? ''}\n${e.stack ?? ''}</pre>
					</div>`
				})
				return false
			}
			return true
		}

		// hardening
		hardening()

		// fps controlling solution based on https://stackoverflow.com/questions/19764018/controlling-fps-with-requestanimationframe
		let fps = 60
		let fpsInterval = 1000 / fps
		let then = Date.now()
		let frame = 0
		let stop = false
		function render() {
			if (stop) return
			requestAnimationFrame(render)

			const now = Date.now()
			const elapsed = now - then

			if (elapsed > fpsInterval) {
				then = now - (elapsed % fpsInterval)

				frame++
				const success = callUserFn(frame / fps)
				if (!success) {
					stop = true
				}
			}
		}
		requestAnimationFrame(render)

		// initial render
		callUserFn(0)
	}
})
