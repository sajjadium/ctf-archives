function showAlert(message) {
    const alertDiv = document.getElementById('alertMessage');
    alertDiv.innerHTML = '<p>' + message + '</p>';
    alertDiv.classList.remove('d-none');
}

document.getElementById("submit").onclick = async function() {
    fetch("./api/login", {
        method: "POST",
        body: JSON.stringify({
            username: document.getElementById("username").value,
            password: document.getElementById("password").value,
        }),
    }).then(async (response) => {
        const body = await response.text()

        try {
            JSON.parse(body)
            showAlert("Logged in!")
        } catch(_) {
            showAlert(body)
        }
    })
}