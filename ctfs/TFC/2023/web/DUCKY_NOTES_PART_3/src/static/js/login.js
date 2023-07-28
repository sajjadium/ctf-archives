$(document).ready(function() {
	$("#login-btn").on('click', function() {
		login()
	});
});

async function login() {

	let message = $("#alert-msg");
	message.hide();

	let username = $("#username").val();
	let password = $("#password").val();

	if ($.trim(username) === '' || $.trim(password) === '') {
		message.text("Missing username or password!");
		message.show();
		return;
	}

	const data = {username: username, password: password};

	await fetch(`/api/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		})
		.then((response) => response.json()
			.then((resp) => {
				if (response.status == 200) {
					window.location.href = '/posts/create';
					return;
				}
				message.text(resp);
				message.show();
			}))
		.catch((error) => {
			message.text(error);
			message.show();
		});
}