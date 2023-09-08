// sample code taken from https://www.dwitter.net/d/18597
const fallback =
	localStorage.savedCode ??
	'with(x)for(i=999;i--;fillRect(~setTransform(s=24e3/i,0,0,4*s,960-i+9*s*C(a=i+60*t),540+8*s*S(a)),~rotate(T(a*a)),2,2))fillStyle=R(9,i/4,i/3)'
let code = new URLSearchParams(location.search).get('code') ?? fallback
localStorage.savedCode = code

const worker = new Worker('worker.js')
worker.addEventListener('message', function (event) {
	if (event.data.type === 'error') {
		document.getElementById('error-output').setHTML(event.data.content)
	}
})
const canvas = document.getElementById('canvas').transferControlToOffscreen()
worker.postMessage({ type: 'init', code, canvas }, [canvas])

const form = document.getElementById('code-form')
form.code.value = code

document.getElementById('btn-reset').addEventListener('click', function () {
	delete localStorage.savedCode
	location = '/'
})
