window.inputBox = document.getElementById('json-input');
window.outputBox = document.getElementById('json-output');
window.container = document.getElementById('container');

const defaults = {
	opts: {
		cols: 4
	},
	debug: false,
};

const beautify = () => {
	try {
		userJson = JSON.parse(inputBox.textContent);
	} catch (e){
		return;
	};

	loadConfig();
	const cols = this.config?.opts?.cols || defaults.opts.cols;
	output = JSON.stringify(userJson, null, cols);

	console.log(this.config?.opts)
	
	if(this.config?.debug || defaults.debug){
		eval(`beautified = ${output}`);
		return beautified;
	};
	
	outputBox.innerHTML = `<pre>${output}</pre>`
};

const saveConfig = (config) => {
	localStorage.setItem('config', JSON.stringify(config));
};

const loadConfig = () => {
	if (localStorage.hasOwnProperty('config')){
		window.config = JSON.parse(localStorage.getItem('config'))
	};
}

console.log('hello from JSON beautifier!')

inputBox.addEventListener("DOMCharacterDataModified", () => {
	beautify();
});

if((new URL(location).searchParams).get('json')){
	const jsonParam = (new URL(location).searchParams).get('json');
	inputBox.textContent = jsonParam;
};

beautify();
