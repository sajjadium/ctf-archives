$(document).ready(function() {
	$("#report-btn").on('click', function() {
		report()
	});
});

async function report() {

	let message = $("#alert-msg");
	message.hide();

	await fetch(`/api/report`, {
			method: 'POST'
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