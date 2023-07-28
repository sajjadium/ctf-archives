$(document).ready(function() {
	$("#send-btn").on('click', function() {
		create()
	});
});

async function create() {

	let message = $("#alert-msg");
	message.hide();

	let title = $("#title").val();
	let content = $("#content").val();
	let hidden = $("#hidden").attr("checked");

	hidden = ((hidden == 1) ? true : false);


	if ($.trim(title) === '' || $.trim(title) === '') {
		message.text("Missing title or content!");
		message.show();
		return;
	}

	const data = {title: title, content: content, hidden: hidden};

	await fetch(`/api/posts`, {
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