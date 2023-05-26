function submitForm(e) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/api' + location.pathname, {
        method: 'POST',
        body: JSON.stringify({ username, password }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(res => {
        if (!res.ok)
            throw res.error;

        localStorage.setItem('sessionId', res.sessionId);
        localStorage.setItem('userId', res.userId);
        redirect();
    }).catch(err => {
        alert(err);
    });

    e.preventDefault();
}

document.querySelector('form').addEventListener('submit', submitForm);

function redirect() {
    if ('sessionId' in localStorage && 'userId' in localStorage)
        window.location = new URLSearchParams(window.location.search).get('next') ?? '/';
}

redirect();
