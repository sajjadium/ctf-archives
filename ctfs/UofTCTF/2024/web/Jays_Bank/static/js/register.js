document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const messageBox = document.getElementById('messageBox');

    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const data = {
            username: registerForm.username.value,
            password: registerForm.password.value
        };

        fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(response => response.json())
        .then(json => {
            showMessage(json.message, json.success ? 'success' : 'error');
            if (json.success) {
                window.location.href = '/login';
            }
        }).catch(error => {
            showMessage('An error occurred. Please try again.', 'error');
        });
    });

    function showMessage(message, type) {
        messageBox.textContent = message;
        messageBox.className = `message-box ${type}`; 
        messageBox.style.display = 'block';
    }
});
