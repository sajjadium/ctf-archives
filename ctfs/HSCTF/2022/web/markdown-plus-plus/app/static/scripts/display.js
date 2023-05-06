let i = 0;
function generate_id() {
	return "id" + i++;
}
function parse(markdown) {
	//TODO implement per-element custom styles
	let stylesheet = [];
	let tree = document.createDocumentFragment();
	while (markdown.length > 0) {
		let node = document.createElement("span");
		let id = generate_id();
		node.id = id;

		let parsed,
			style = "",
			sub_stylesheet = [];

		if (markdown.startsWith("[b ")) {
			// bold
			style = "font-weight: bold";

			[parsed, markdown, sub_stylesheet] = parse(markdown.substring(3));
		} else if (markdown.startsWith("[i ")) {
			// italics
			style = "font-style: italic";

			[parsed, markdown, sub_stylesheet] = parse(markdown.substring(3));
		} else if (markdown.startsWith("[` ")) {
			// code
			style = `background-color: #eee;
			border-radius: 3px;
			font-family: monospace;
			padding: 0 3px;`;

			[parsed, markdown, sub_stylesheet] = parse(markdown.substring(3));
		} else if (markdown.startsWith("[u ")) {
			// underline
			style = "text-decoration: underline";

			[parsed, markdown, sub_stylesheet] = parse(markdown.substring(3));
		} else if (markdown.startsWith("[s ")) {
			// strikethrough
			style = "text-decoration: line-through";

			[parsed, markdown, sub_stylesheet] = parse(markdown.substring(3));
		} else if (markdown.startsWith("[c=")) {
			// color
			markdown = markdown.substring(3);

			let arr = markdown.split(" ");
			let color = arr.shift();
			markdown = arr.join(" ");
			style = "color:" + color;

			[parsed, markdown, sub_stylesheet] = parse(markdown);
		} else if (markdown.startsWith("[h=")) {
			// highlight
			markdown = markdown.substring(3);

			let arr = markdown.split(" ");
			let color = arr.shift();
			markdown = arr.join(" ");
			style = "background-color:" + color;

			[parsed, markdown, sub_stylesheet] = parse(markdown);
		} else if (markdown.startsWith("[a=")) {
			// links
			markdown = markdown.substring(3);

			parsed = document.createElement("a");
			let arr = markdown.split(" ");
			let href = arr.shift();
			markdown = arr.join(" ");
			parsed.href = href;

			let content;
			[content, markdown, sub_stylesheet] = parse(markdown);
			parsed.append(content);
		} else if (markdown.startsWith("]")) {
			// end tag
			return [tree, markdown.substring(1), stylesheet];
		} else {
			// match up to the next unescaped [ or ]
			var [_, text, markdown] = markdown.match(/^((?:(?![^\\][[\]]).)*.?)(.*)/);
			parsed = document.createTextNode(text);
		}

		node.append(parsed);
		stylesheet.push(`${id}{${style};}`);
		stylesheet.push(...sub_stylesheet);
		tree.append(node);
	}
	return [tree, "", stylesheet];
}

function display() {
	let markdown = atob(location.hash.substring(1));

	let [el, _, stylesheet] = parse(markdown);

	document.getElementById("root").appendChild(el);

	let style = document.createElement("style");
	style.textContent = stylesheet.join("\n");
	document.head.appendChild(style);
}
display();
