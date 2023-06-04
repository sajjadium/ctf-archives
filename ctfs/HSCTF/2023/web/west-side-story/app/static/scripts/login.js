let form = document.getElementById("login");
form.addEventListener("submit", async function (event) {
	event.preventDefault();

	let form_data = new FormData(form);
	let data = JSON.stringify({
		user: form_data.get("user"),
		password: form_data.get("password"),
	});

	let response = await fetch("/api/login", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: data,
	});

	if (response.ok) {
		window.location = "/";
	} else {
		let error = (await response.json()).error;
		document.getElementById("error").style.display = "block";
		document.getElementById("error").textContent = error;
	}
});
