import { default as Arg } from "https://cdn.jsdelivr.net/npm/@vunamhung/arg.js@1.4.0/+esm";
import { default as insane } from "https://cdn.jsdelivr.net/npm/insane@2.6.2/+esm";

const options = {
	allowedAttributes: {
		a: ["href"],
		abbr: ["title"],
		details: ["open"],
		"*": ["id", "dir"],
	},
	allowedClasses: {},
	allowedSchemes: ["http", "https"],
	allowedTags: [
		"a",
		"abbr",
		"article",
		"b",
		"blockquote",
		"br",
		"code",
		"del",
		"details",
		"div",
		"em",
		"h1",
		"h2",
		"h3",
		"h4",
		"h5",
		"h6",
		"hr",
		"i",
		"img",
		"ins",
		"kbd",
		"li",
		"main",
		"mark",
		"ol",
		"p",
		"pre",
		"q",
		"s",
		"section",
		"small",
		"span",
		"strike",
		"strong",
		"sub",
		"summary",
		"sup",
		"u",
		"ul",
	],
	filter: null,
	transformText: null,
};

let title = document.getElementById("title");
let content = document.getElementById("content");

function display() {
	title.textContent = Arg("title");
	document.title = Arg("title");

	let sanitized = insane(Arg("content"), options, true);
	content.innerHTML = sanitized;

	document.body.style.backgroundColor = Arg("background_color");
	document.body.style.color = Arg("color");
	document.body.style.fontFamily = Arg("font");
	content.style.fontSize = Arg("font_size") + "px";
}

display();
