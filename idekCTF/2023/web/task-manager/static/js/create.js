window.addEventListener("load", () => {
	document.querySelector("#create-task-form").addEventListener("submit", async e => {
		e.preventDefault();
		let formData = Object.fromEntries(
			new FormData(e.target)
		);

		await fetch("/api/manage_tasks", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(formData)
		})
			.then(async r => {
				if (r.status !== 200) {
					let { message } = await r.json();
					alert(message);
				}
				else {
					window.location.href = "/home.html";
				}
			});

	})
})