const render = document.getElementById('render');
const output = document.getElementById('output');
const input = document.getElementById('content');

render.onclick = async e => {
	let res = await (await fetch(`/render?content=${encodeURIComponent(input.value)}`)).text();
	output.innerHTML = res;
	MathJax.Hub.Typeset();
}
