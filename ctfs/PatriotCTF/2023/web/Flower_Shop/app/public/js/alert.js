function displayAlert(message) {
    alert(message);
}

const urlParams = new URLSearchParams(window.location.search);
const error = urlParams.get('error');
const msg = urlParams.get('msg');

if (error) {
    displayAlert(error);
} else if (msg) {
    displayAlert(msg);
}
