function fancify(note) {
	color = (args.style || Math.floor(Math.random() * 6)).toString();
	image = this.image || '/static/images/success.png';
	styleElement = note.children[2];
	styleElement.innerHTML = style; // i have no idea why i did this in such a scuffed way but I'm too lazy to change it. no this is not vulnerable
	note.className = `animation${color}`;
	img = new Image();
	img.src = image
	note.append(img);
}

args = Arg.parse(location.search);
noteElement = document.getElementById('note');

if(noteElement){
	fancify(noteElement);
}
