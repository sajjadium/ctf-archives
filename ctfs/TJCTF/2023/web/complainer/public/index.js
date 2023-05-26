fetch('/api/verify', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${localStorage.getItem('userId')}:${localStorage.getItem('sessionId')}`
    }
}).then(res => res.json()).then(res => {
    if (!res.ok)
        throw res.error;
}).catch(_ => {
    localStorage.removeItem('sessionId');
    localStorage.removeItem('userId');
    window.location = '/login';
});

function submitForm(e) {
    fetch('/api/post', {
        method: 'POST',
        body: JSON.stringify({
            body: document.getElementById('body').value
        }),
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('userId')}:${localStorage.getItem('sessionId')}`
        }
    }).then(res => res.json()).then(res => {
        if (res.error)
            throw res.error;

        window.location = '/post/' + res.postId;
    }).catch(err => {
        alert(err);
        window.location = '/login';
    });

    e.preventDefault();
}

document.querySelector('form').addEventListener('submit', submitForm);
