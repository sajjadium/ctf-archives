function create(e) {
	e.preventDefault();
	window.location = "/display#" + btoa(document.getElementById("content").value);
}

document.getElementById("content-form").addEventListener("submit", create);
