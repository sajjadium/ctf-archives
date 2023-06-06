import { default as Arg } from "https://cdn.jsdelivr.net/npm/@vunamhung/arg.js@1.4.0/+esm";

let form = document.getElementById("content-form");
function create(e) {
	e.preventDefault();
	window.location = Arg.url("/display.html", Object.fromEntries(new FormData(form)));
}

form.addEventListener("submit", create);
