const refreshPosts = async (searchValue = "") => {
	const wall = document.getElementById("content-box");
	while (wall.firstChild) {
		wall.removeChild(wall.firstChild);
	}
	const res = await fetch(`/api/post/wall?q=${encodeURI(searchValue)}`, {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			Accept: "application/json",
			Cookie: document.cookie,
		},
	});
	if (res.status !== 200) {
		window.location.href = "/error?message=Something went wrong";
	}
	const { data, count } = await res.json();
	for (let i = 0; i < count; i++) {
		let p = document.createElement("iframe");
		p.src = `/api/post/${data[i]}`;
		p.style.width = "100%";
		p.style.height = "100%";
		p.style.border = "none";
		p.style.display = "none";
		wall.appendChild(p);
		p.onload = () => {
			if (p.contentDocument.body.innerText === "404") {
				p.remove();
			} else {
				p.style.display = "block";
			}
		};
	}
};
let hasBeenIdleFor3Seconds = false;
let newTyping = false;
window.addEventListener("DOMContentLoaded", async () => {
	await refreshPosts();

	document.getElementById("search-input").addEventListener("input", (e) => {
		newTyping = true;
		hasBeenIdleFor3Seconds = false;
	});

	setInterval(() => {
		hasBeenIdleFor3Seconds = true;
		if (newTyping) {
			const query = document.getElementById("search-input").value;
			refreshPosts(query);
		}
		newTyping = false;
	}, 3000);
});
