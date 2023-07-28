$(document).ready(function() {
	$("#register-btn").on('click', function() {
		register()
	});
});

async function register() {

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

	await fetch(`/api/register`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify(data),
		})
		.then((response) => response.json()
			.then((resp) => {
				message.text(resp);
				message.show();
			}))
		.catch((error) => {
			message.text(error);
			message.show();
		});
}