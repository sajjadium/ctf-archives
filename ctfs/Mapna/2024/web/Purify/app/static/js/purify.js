async function init() {
	window.wasm = (await WebAssembly.instantiateStreaming(
		fetch('./purify.wasm')
	)).instance.exports
}

function sanitize(dirty) {
	wasm.set_mode(0)	

	for(let i=0;i<dirty.length;i++){
		wasm.add_char(dirty.charCodeAt(i))
	}

	let c
	let clean = ''
	while((c = wasm.get_char()) != 0){
		clean += String.fromCharCode(c)
	}

	return clean
}

window.DOMPurify = { 
	sanitize,
	version: '1.3.7'
}

init()
