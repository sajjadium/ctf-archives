document.getElementById('submit-button').onclick = e=>{
	let selectEl = document.getElementById('todo-select');
	let frameEl = document.getElementById('results-frame');
	let selectedTodo = selectEl.selectedOptions[0].innerText;
	frameEl.src += selectedTodo+'/';
}

document.getElementById('results-frame').onload = e=>{
	let frameEl = document.getElementById('results-frame');
	let t = frameEl.contentWindow.document.body.innerText;
	if(t.indexOf('Error') > -1) document.location = '/';
}

(()=>{
	let frameEl = document.getElementById('results-frame').src = './render/';
})()

