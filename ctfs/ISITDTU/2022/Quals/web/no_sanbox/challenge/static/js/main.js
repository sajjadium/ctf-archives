document.getElementById('form').addEventListener('submit', e => {
	e.preventDefault();

	fetch('/api/submit', {
		method: 'POST',
		body: JSON.stringify({
			'artist.name': document.querySelector('input[type=text]').value
		}),
		headers: {'Content-Type': 'application/json'}
	})
	.then(resp => resp.json())
	.then(data => {
		document.getElementById('output').innerHTML = data.response;
	});
});