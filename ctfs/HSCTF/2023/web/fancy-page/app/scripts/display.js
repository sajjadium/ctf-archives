import { default as Arg } from "https://cdn.jsdelivr.net/npm/@vunamhung/arg.js@1.4.0/+esm";

function sanitize(content) {
	return content.replace(/script|on|iframe|object|embed|cookie/gi, "");
}

let title = document.getElementById("title");
let content = document.getElementById("content");

function display() {
	title.textContent = Arg("title");
	document.title = Arg("title");

	let sanitized = sanitize(Arg("content"));
	content.innerHTML = sanitized;

	document.body.style.backgroundColor = Arg("background_color");
	document.body.style.color = Arg("color");
	document.body.style.fontFamily = Arg("font");
	content.style.fontSize = Arg("font_size") + "px";
}

display();
