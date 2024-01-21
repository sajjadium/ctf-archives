window.onmessage = e=>{
	list.innerHTML += `
		<li>From ${e.origin}: ${window.DOMPurify.sanitize(e.data.toString())}</li>
	`
}

setTimeout(_=>window.postMessage("hi",'*'),1000)
