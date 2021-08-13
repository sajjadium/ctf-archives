let area = document.getElementById("safe")

window.addEventListener("message", (event) => {
    console.log("Previewing..")
	let raw = event.data

	fetch("/api/filter", {
		method: "POST",
		credentials: "include",
		body: JSON.stringify({
			raw: raw
		})
	})
    .then(resp => resp.json())
	.then(response => {
		console.log("Filtered")
		document.body.innerHTML = response.Sanitized
		window.parent.postMessage(response, "*"); 
	}); 
}, false);
