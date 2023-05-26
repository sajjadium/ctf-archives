fetch('/api/logout', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('userId')}:${localStorage.getItem('sessionId')}`
    }
}).then(() => {
    localStorage.removeItem('userId');
    localStorage.removeItem('sessionId');
    window.location.href = '/login';
});
