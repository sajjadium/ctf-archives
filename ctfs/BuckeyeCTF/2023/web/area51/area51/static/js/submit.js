const login = document.getElementById('login');
const response = document.getElementById('response');

login.addEventListener('submit', e => {
	e.preventDefault();

	fetch('/api/login', {
		method: 'POST',
		body: new URLSearchParams(new FormData(e.target))
	})
        .then(resp => resp.json())
        .then(data => {
            response.innerHTML = data.message;
	});
});