const refreshFriends = async () => {
	const friendsBox = document.getElementById("friends-box");
	while (friendsBox.firstChild) {
		friendsBox.removeChild(friendsBox.firstChild);
	}
	const res = await fetch("/api/user/friends", {
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

	const friendsNames = await res.json();
	friendsNames.forEach((friend) => {
		const p = document.createElement("p");
		p.innerText = friend;
		friendsBox.appendChild(p);
	});
};

window.addEventListener("DOMContentLoaded", async () => {
	await refreshFriends();

	document
		.getElementById("add-friend-button")
		.addEventListener("click", async () => {
			const inputBox = document.getElementById("friend-name");
			const friendName = inputBox.value;
			const res = await fetch("/api/user/friends", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					Accept: "application/json",
					Cookie: document.cookie,
				},
				body: JSON.stringify({ username: friendName }),
			});
			if (res.status !== 200) {
				window.location.href = "/error?message=Something went wrong";
			}
			if (res.redirected) {
				window.location.href = res.url;
			}

			inputBox.value = "";
			await refreshFriends();
		});
});
