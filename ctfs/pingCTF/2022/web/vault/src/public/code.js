VAULT.addEventListener("submit", async (e) => {
	e.preventDefault();
	alert(
		await (
			await fetch("/api/set", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					content: content.value,
					password: password.value,
				}),
			})
		).text()
	);
});
window.addEventListener("load", async () => {
	if (document.location.search == "?reveal") {
		var password = prompt("Provide secret password:");
		secret.innerText =
			"Your secret: " +
			(await (await fetch(`/api/get?password=${password}`)).text());
	}
});

REPORT.addEventListener("click", async () => {
	var url = prompt("Provide bug url:");
	alert(await (await fetch(`/report?url=${url}`)).text());
});
